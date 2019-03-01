for i in $(seq 1 100);
do
    python simulator.py 1
    rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi
done