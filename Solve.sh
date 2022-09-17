now="$(date +'%M:%S')"
echo "Start time ex 1: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar 33gw.dpomdp -h4 > gw.log
now="$(date +'%M:%S')"
echo "Start time ex 2: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar 33gw-nocomm.dpomdp -h4 > gw2.log
now="$(date +'%M:%S')"
echo "Start time ex 3: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar 33gw-late.dpomdp -h4 > gw3.log
now="$(date +'%M:%S')"
echo "End time ex 3: $now"
