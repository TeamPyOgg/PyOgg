for f in *.py
do
    echo 
    echo "Running example $f:"
    python $f
    if [ $? -ne 0 ]
    then
       exit 1
    fi
done;
        
