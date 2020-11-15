for f in *.py
do
    echo
    if [[ $f == *play* ]]; then
        echo "Skipping example $f because it plays audio"
        continue
    fi
    echo "Running example $f:"
    python $f
    if [ $? -ne 0 ]
    then
       exit 1
    fi
done;
        
