#!/bin/bash

set -e

function extract {
  local file="$1"
 
  local newFile="${file/[.]jpg/.mp4}"

  if [[ -f "$newFile" ]]; then
    echo "File $newFile exists, so ignoring $file"
  else
    #old old  find the offset of the string 'ftypmp42' in the file
    #old old local lines=( $(grep --only-matching --byte-offset --binary --text ftypmp42  $file| cut -f 1 -d:) )
    local lines=( $(grep -Pao 'Length="[^"]*"' $file | cut -d= -f2 | tr -d '"' | tail -n 1))
   
    local totalsize=( $(wc $file | awk '{print $3}'))

    local offset=$(( $totalsize - $lines))
   
    # extract everything beginning at offset to another file
    #tail -c +$offset "$file" > "$newFile"
    dd if=$file of=$newFile bs=$offset skip=1
   
  fi
}

for f in "$@"; do
  #if [[ "$f" == MVIMG*jpg ]]; then
  extract "$f"
  #else
  #  echo "Ignoring $f because its file name does not match MVIMG*jpg pattern"
  #fi
done
