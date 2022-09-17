now="$(date +'%M')"
echo "Start time ex 1: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar --BGIP_Solver=BnB --BnB-ordering=Prob  -Q QMDP --useQcache 33gw.dpomdp -h4
now="$(date +'%M')"
echo "Start time ex 2: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar --BGIP_Solver=BnB --BnB-ordering=Prob  -Q QMDP --useQcache 33gw-nocomm.dpomdp -h4
now="$(date +'%M')"
echo "Start time ex 3: $now"
../MADP/src/solvers/GMAA --sparse --GMAA=MAAstar --BGIP_Solver=BnB --BnB-ordering=Prob  -Q QMDP --useQcache 33gw-late.dpomdp -h4
now="$(date +'%M')"
echo "End time ex 3: $now"
