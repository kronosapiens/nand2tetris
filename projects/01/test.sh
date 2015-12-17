for file in projects/01/*.tst
do
  echo ""
  echo "$file"
  tools/HardwareSimulator.sh "$file"
done