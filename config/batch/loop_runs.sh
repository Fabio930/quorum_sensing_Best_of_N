#! /bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: loop_runs.sh (from src folder) <base_config_dir> <base_config_file_name>"
    exit 1
fi

wdir=`pwd`
base_config=$1$2
if [ ! -e $base_config ]; then
    base_config=$wdir/$1/$2
    if [ ! -e $base_config ]; then
        echo "Error: missing configuration file '$base_config'" 1>&2
        exit 1
    fi
fi

###########################################

model="majority voter"
rebroadcast="no" # static centralized decentralized
num_agents="100"
num_options="2 3 5"
r_type="centralized" # static decentralized
eta="0.2 0.4 0.6 0.8"
quorum_list_min="8"
message_timeout="6"
messages_per_step="5"

for agents in $num_agents; do
    for mdl in $model; do
        for rebrcts in $rebroadcast; do
            if [[ $rebrcts == "static" || $rebrcts == "centralized" || $rebrcts == "decentralized" ]]; then
                message_hops="10 20 30"
            else
                message_hops="1"
            fi
            for options in $num_options; do
                for type in $r_type; do
                    if [[ $type == "centralized" || $type == "decentralized" ]]; then
                        r_val="0.5"
                    else
                        r_val="0.2 0.4 0.6 0.8"
                    fi
                    for val in $r_val; do
                        for et in $eta; do
                            for qlm in $quorum_list_min; do
                                for mt in $message_timeout; do
                                    for ms in $messages_per_step; do
                                        for mh in $message_hops; do
                                            config=`printf 'config__Nrobots_%s__model_%s__rebroadcast_%s__Noptions_%s__Rtype_%s__Rval_%s__eta_%s__minBuff_%s__msgTime_%s__msgXstep_%s__msgHops_%s.xml' $agents $mdl $rebrcts $options $type $val $et $qlm $mt $ms $mh`
                                            cp $base_config $config
                                            sed -i "s|__NUM_AGENTS__|$agents|g" $config
                                            sed -i "s|__NUM_OPTIONS__|$options|g" $config
                                            sed -i "s|__REBROADCAST__|$rebrcts|g" $config
                                            sed -i "s|__MODEL__|$mdl|g" $config
                                            sed -i "s|__R_TYPE__|$type|g" $config
                                            sed -i "s|__R_VAL__|$val|g" $config
                                            sed -i "s|__ETA__|$et|g" $config
                                            sed -i "s|__QUORUM_LIST_MIN__|$qlm|g" $config
                                            sed -i "s|__MSG_TIMEOUT__|$mt|g" $config
                                            sed -i "s|__MSG_X_STEP__|$ms|g" $config
                                            sed -i "s|__MSG_HOPS__|$mh|g" $config
                                            cd ./.venv
                                            python3 ../src/main.py -c '../'$config
                                            cd ../
                                            echo
                                            rm *config__*.xml
                                        done
                                    done
                                done
                            done
                        done
                    done
                done
            done
        done
    done
done