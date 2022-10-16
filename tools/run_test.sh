cd test
for tg in "$@" 
do 
    make FIR_TARGET=$tg; 
    make clean; 
done
cd ..
