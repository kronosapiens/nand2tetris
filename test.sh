assemble=false

if [ $1 -le 3 ]
then
  cmd="tools/HardwareSimulator.sh"
elif [ $1 -eq 4 ]
then
  cmd="tools/CPUEmulator.sh"
  assemble=true
elif [ $1 -eq 5 ]
then
  cmd="tools/HardwareSimulator.sh"
else
  echo "Unknown project"
fi

if [ $2 ]
then
  path=$1/$2
else
  path=$1
fi

if [ $assemble ]
then
  for file in projects/$path/*.asm
  do
    echo
    echo "Assembling $file"
    tools/Assembler.sh $file
  done
fi

for file in projects/$path/*.tst
do
  echo
  echo "Testing $file"
  $cmd $file
done