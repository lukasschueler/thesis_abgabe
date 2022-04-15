#!/bin/bash

activate () {
    source ./"$1"/bin/activate
}

joinByChar() {
  local IFS=" "
  shift
  args="$*"
}

startTrainingRun() {
directory="$1"
venv="$2"
command="$3"
setting="$4"

joinByChar "${setting[@]}"

echo "Changing to Directory of Architecture in Question: "
cd "$directory" || echo "Failure moving into""$directory"

echo "Activating venv..."
activate "$venv" || echo "Could not activate ""$venv""!"

eval "python $command $args" || echo 'Failure starting the A.I.'
echo "Finished training!"
echo "Deactivating venv and moving back to training base."
deactivate
cd .. 
}

checkPosition() {
echo 'Checking Position...'
if [ "$1" = "$2" ]
then
    echo 'Starting from correct directory.'
else
    echo 'Starting from wrong directory!'
    echo 'Should be'"$2"'.'
    echo 'Exit.'
    # exit 1    
fi
}

#Directories
currentPosition=$PWD
#TODO: Correct that after debugging
targetPosition='/home/luki/Documents/thesis/code'

#Check correct positioning
checkPosition "$currentPosition" "$targetPosition"

#Here the scenarios in question are read
#TODO:Correct that one after debugging too
readarray -t settings < /home/luki/Documents/thesis/code/configTraining/configurations.txt



#Here these scenarios are executed
for line in "${settings[@]}"
    do
        read -a setting <<< $line
        case "${setting[0]}" in

      ppo)
        dir='./proximal_policy_optimization'
        venv="ppo"
        cmd='run.py'
        startTrainingRun "$dir" "$venv" "$cmd" "${setting[@]}"
        ;;

      rnd)
        dir='./rndRobustness'
        venv="rnd"
        cmd='run_atari.py'
        startTrainingRun "$dir" "$venv" "$cmd" "${setting[@]}"        
        ;;

      novar)
        dir='./disagreementnoVariance'
        venv="novariance"
        cmd='run.py'
        startTrainingRun "$dir" "$venv" "$cmd" "${setting[@]}"        
        ;;      

      disagree)
        dir='./disagreementRobustness'
        venv="disagreement"
        cmd='run.py'
        startTrainingRun "$dir" "$venv" "$cmd" "${setting[@]}"        
        ;;

      *)
        echo -n "The specified architecture does not exist on that hardware!"
        echo "${setting[0]}"
        # exit 1
        ;;
    esac
done



