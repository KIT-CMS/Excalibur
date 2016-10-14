if [ "$1" == "sg" ]
	then
	condor_status -constraint 'CLOUDSITE=="ekpsupermachines"' #-state -total
elif [ "$1" == "sg01" ]
	then
	condor_status -constraint 'machine=="ekpsg01.physik.uni-karlsruhe.de"' -state -total
elif [ "$1" == "sg02" ]
	then
	condor_status -constraint 'machine=="ekpsg02.physik.uni-karlsruhe.de"' -state -total
elif [ "$1" == "s03g" ]
	then
	condor_status -constraint 'machine=="ekpsg03.physik.uni-karlsruhe.de"' -state -total
elif [ "$1" == "sg04" ]
	then
	condor_status -constraint 'machine=="ekpsg04.physik.uni-karlsruhe.de"' -state -total
elif [ "$1" == "sm01" ]
	then
	condor_status -constraint 'machine=="ekpsm01.physik.uni-karlsruhe.de"' -state -total
elif [ "$1" == "bw4" ]
	then
	condor_status -constraint 'CLOUDSITE=="BWFORCLUSTER"' -state -total
else
	echo 'no machine type given!'
	exit 1
fi
