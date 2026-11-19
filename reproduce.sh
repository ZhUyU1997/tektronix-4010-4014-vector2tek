#!/usr/bin/env bash
# Reproduce the 227 Tek pages recorded in sources.tsv.
#
#   ./reproduce.sh                 rebuild every tek/<id>.tek in place
#   ./reproduce.sh --check         rebuild into work/repro,
#                                  cmp -s each result, and leave tek/ untouched
#   ./reproduce.sh --list          print the 227 commands from sources.tsv
#   ./reproduce.sh --only ID       run one page; combine with --check
#
# Every row of sources.tsv is one complete shell command.  The converters
# need the packages in vector2tek/requirements.txt; byte-exact vector output
# needs PyMuPDF 1.28.2 and the CAD pages need ezdxf 1.4.5.
set -u

# Keep the archive free of __pycache__ directories.
export PYTHONDONTWRITEBYTECODE=1

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
TSV=$ROOT/sources.tsv
ARCHIVE=$ROOT/tek
WORK=$ROOT/work/repro
EXPECTED=227

CHECK=0
LIST=0
ONLY=

usage() {
    cat <<'EOF'
usage: ./reproduce.sh [--check] [--list] [--only ID]

  (no option)  rebuild tek/<id>.tek in place
  --check      rebuild into a scratch dir and compare byte-for-byte with cmp -s
  --list       print the per-page commands only
  --only ID    restrict to one page (works with --check)
EOF
}

while [ $# -gt 0 ]; do
    case $1 in
        --check) CHECK=1 ;;
        --list) LIST=1 ;;
        --only)
            [ $# -ge 2 ] || { echo "reproduce.sh: --only needs an id" >&2; exit 2; }
            ONLY=$2
            shift
            ;;
        --only=*) ONLY=${1#*=} ;;
        -h|--help) usage; exit 0 ;;
        *) echo "reproduce.sh: unknown argument: $1" >&2; usage >&2; exit 2 ;;
    esac
    shift
done

[ -f "$TSV" ] || { echo "reproduce.sh: missing $TSV" >&2; exit 1; }
rows=$(awk -F'\t' 'NR > 1 && $1 != "" { n++ } END { print n + 0 }' "$TSV")
[ "$rows" -eq "$EXPECTED" ] || {
    echo "reproduce.sh: $TSV has $rows data rows, expected $EXPECTED" >&2
    exit 1
}

if [ "$LIST" -eq 1 ]; then
    awk -F'\t' -v only="$ONLY" '
        NR > 1 && $1 != "" && (only == "" || $1 == only) { print $6 }
    ' "$TSV"
    exit 0
fi

[ "$CHECK" -eq 1 ] && mkdir -p "$WORK"

total=0
ok=0
bad=0
failed=0
missing=0

while IFS=$'\t' read -r id source command; do
    [ -n "$id" ] || continue
    [ -n "$ONLY" ] && [ "$id" != "$ONLY" ] && continue
    total=$((total + 1))

    if [ ! -f "$ROOT/$source" ]; then
        printf 'MISS %-28s %s\n' "$id" "$source"
        missing=$((missing + 1))
        continue
    fi

    if [ "$CHECK" -eq 1 ]; then
        archive_ref="\$HOME/tek-resource/tek/$id.tek"
        work_ref="$WORK/$id.tek"
        case $command in
            *"$archive_ref"*) ;;
            *)
                printf 'FAIL %-28s command has no archive output path\n' "$id"
                failed=$((failed + 1))
                continue
                ;;
        esac
        run=${command//"$archive_ref"/"$work_ref"}
        : > "$work_ref"
    else
        run=$command
    fi

    if ! bash -c "$run"; then
        printf 'FAIL %-28s conversion command failed\n' "$id"
        failed=$((failed + 1))
        continue
    fi

    if [ "$CHECK" -eq 1 ]; then
        if [ -f "$work_ref" ] && cmp -s "$work_ref" "$ARCHIVE/$id.tek"; then
            printf 'OK   %-28s %8d B\n' "$id" "$(wc -c < "$work_ref")"
            ok=$((ok + 1))
        else
            new_bytes=$(wc -c < "$work_ref" 2>/dev/null || echo 0)
            old_bytes=$(wc -c < "$ARCHIVE/$id.tek" 2>/dev/null || echo 0)
            printf 'DIFF %-28s new=%s old=%s\n' "$id" "$new_bytes" "$old_bytes"
            bad=$((bad + 1))
        fi
    else
        if [ -s "$ARCHIVE/$id.tek" ]; then
            printf 'WROTE %-27s %8d B\n' "$id" "$(wc -c < "$ARCHIVE/$id.tek")"
            ok=$((ok + 1))
        else
            printf 'FAIL %-28s no output\n' "$id"
            failed=$((failed + 1))
        fi
    fi
done < <(awk -F'\t' 'NR > 1 && $1 != "" { printf "%s\t%s\t%s\n", $1, $3, $6 }' "$TSV")

echo
echo "pages=$total identical=$ok different=$bad failed=$failed missing=$missing"

if [ -n "$ONLY" ] && [ "$total" -eq 0 ]; then
    echo "reproduce.sh: no page with id '$ONLY'" >&2
    exit 1
fi
if [ -z "$ONLY" ] && [ "$total" -ne "$EXPECTED" ]; then
    echo "reproduce.sh: ran $total pages, expected $EXPECTED" >&2
    exit 1
fi
if [ "$missing" -ne 0 ] || [ "$failed" -ne 0 ]; then
    exit 1
fi
if [ "$CHECK" -eq 1 ] && [ "$bad" -ne 0 ]; then
    exit 1
fi
exit 0
