@echo off
if not exist %1 mkdir %1
python -m pixelsort "sort/%~2" -o "%~1/c10.png" -i random -c 10
python -m pixelsort "sort/%~2" -o "%~1/c20.png" -i random -c 20
python -m pixelsort "sort/%~2" -o "%~1/thalf.png" -i random -t .5
python -m pixelsort "sort/%~2" -o "%~1/c2090.png" -i random -c 20 -a -90
python -m pixelsort "sort/%~2" -o "%~1/c200-90.png" -i random -c 200 -a -90
python -m pixelsort "sort/%~2" -o "%~1/c100.png" -i random -c 100