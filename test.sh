for file in projects/$1/*.tst
do
  echo ""
  echo "$file"
  tools/HardwareSimulator.sh "$file"
done