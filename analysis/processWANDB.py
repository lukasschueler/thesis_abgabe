

def dataProcessing(data):
    counter = 0
    for run in data:
        # if "processed" not in run.tags:
        if True:
            problemsInRun = {}
            # processable, problemsInRun = addArchitectureTag(run, problemsInRun)
            if "ppo" not in run.tags:
                problemsInRun = addRewardTag(run, problemsInRun)
                problemsInRun = addEnvironmentTag(run, problemsInRun)
                problemsInRun = addTimestepTag(run, problemsInRun)
                problemsInRun = addExtraNoiseTag(run, problemsInRun)
                problemsInRun = addRandomActionTag(run, problemsInRun)
                problemsInRun = addFETag(run, problemsInRun)
                problemsInRun = addPolicyTag(run, problemsInRun)
                problemsInRun = addFramestackTag(run, problemsInRun)
                problemsInRun = addCoverageTag(run, problemsInRun)
                problemsInRun = addActionDependencyTag(run, problemsInRun)
                
            if not problemsInRun:
                run.tags.append("processed")
                counter +=1
            else:
                with open('/home/luki/Documents/thesis/analysis/issues/' + run.name + '.txt', 'w') as convert_file:
                    convert_file.write(json.dumps(problemsInRun))
            try:
                run.update()
            except:
                print(run.name)
                print(run.id)
                print(run.config["num_timesteps"])
                print(type(run.config["num_timesteps"]))
                print()
        else:
            counter += 1
        result = '{} of {} sucessfully processed.'.format(counter, len(runs))
        print(result)
       
def addPolicyTag(run, problemsInRun):
    target = "policy"
    if target in run.config:
        marker = run.config[target]
        if marker == "cnn":
            if "cnn" not in run.tags:
                run.tags.append("cnn") 

        elif marker == "rnn":
            if "rnn" not in run.tags:
                run.tags.append("rnn") 
                
        else:
            print("The Policy for the run in question was not assignable:")
            print("ID: " + run.id)
            print("Name: " + run.name)
            if run.id in problemsInRun:
                issues = problemsInRun[run.id]
                issues.append(target)
            else:
                problemsInRun[run.id] = [target]
    return problemsInRun


def addFramestackTag(run, problemsInRun):
    target = "frame_stack"
    if target in run.config:
        marker = int(run.config[target])
        if marker == 4:
            if "FS" not in run.tags:
                run.tags.append("FS") 

        elif marker == 1:
            if "NoFS" not in run.tags:
                run.tags.append("NoFS") 
                
        else:
            print("The frame_stack for the run in question was not assignable:")
            print("ID: " + run.id)
            print("Name: " + run.name)
            if run.id in problemsInRun:
                issues = problemsInRun[run.id]
                issues.append(target)
            else:
                problemsInRun[run.id] = [target]
    return problemsInRun
    
    
    
def addFETag(run, problemsInRun):
    target = "feat_learning"
    if target in run.config:
        marker = run.config[target]
        if marker == "idf":
            if "idf" not in run.tags:
                run.tags.append("idf") 

        elif marker == "vaesph":
            if "vaesph" not in run.tags:
                run.tags.append("vaesph") 

        elif marker == "none":
            if "random" not in run.tags:
                run.tags.append("random") 

        elif marker == "vaenonsph":
            if "vaenonsph" not in run.tags:
                run.tags.append("vaenonsph") 
                
        else:
            print("The Extractor for the run in question was not assignable:")
            print("ID: " + run.id)
            print("Name: " + run.name)
            if run.id in problemsInRun:
                issues = problemsInRun[run.id]
                issues.append(target)
            else:
                problemsInRun[run.id] = [target]
    return problemsInRun

def addArchitectureTag(run, problemsInRun):
    target = "architecture"
    marker = run.config[target]
    if marker == "ppo":
        if "ppo" not in run.tags:
            run.tags.append("ppo")
            
        return False, problemsInRun

    elif marker == "rnd":
        if "rnd" not in run.tags:
            run.tags.append("rnd") 
        return True, problemsInRun

    elif marker == "disagree":
        if "disagree" not in run.tags:
            run.tags.append("disagree") 
        return True, problemsInRun
            
    elif marker == "curiosity":
        if "curiosity" not in run.tags:
            run.tags.append("curiosity") 
        return True, problemsInRun
            
    else:
        print("The architecture for the run in question was not assignable:")
        print("ID: " + run.id)
        print("Name: " + run.name)
        if run.id in problemsInRun:
            issues = problemsInRun[run.id]
            issues.append(target)
        else:
            problemsInRun[run.id] = [target]
            return False, problemsInRun
            
    
def addRewardTag(run, problemsInRun):
    target = "reward"
    if "ext_coeff" in run.config and "int_coeff" in run.config:
        ext_reward = int(run.config["ext_coeff"])
        int_reward = int(run.config["int_coeff"])
        if ext_reward == 1 and int_reward == 1:
            if "BothRewards" not in run.tags:
                run.tags.append("BothRewards") 
        elif ext_reward == 1 and int_reward == 0:
            if "Extrinsic" not in run.tags:
                run.tags.append("Extrinsic") 
        elif ext_reward == 0 and int_reward == 1:
            if "Intrinsic" not in run.tags:
                run.tags.append("Intrinsic") 
        else:
            print("The reward signal for the run in question was not assignable:")
            print("ID: " + run.id)
            print("Name: " + run.name)
            if run.id in problemsInRun:
                issues = problemsInRun[run.id]
                issues.append(target)
            else:
                problemsInRun[run.id] = [target]
    else:
        print("The reward signal for the run in question was not assignable:")
        print("ID: " + run.id)
        print("Name: " + run.name)
        if run.id in problemsInRun:
            issues = problemsInRun[run.id]
            issues.append(target)
        else:
            problemsInRun[run.id] = [target]
    return problemsInRun

def addEnvironmentTag(run, problemsInRun):
    target = "env"
    if target in run.config:
        env = run.config[target]
        if env == "MiniGrid-DoorKey-8x8-v0":
            if "8x8" not in run.tags:
                run.tags.append("8x8") 
        elif env == "MiniGrid-RandomColours-8x8-v0":
            if "8Bx8B" not in run.tags:
                run.tags.append("8Bx8B") 
        elif env == "MiniGrid-DoorKey-16x16-v0":
            if "16x16" not in run.tags:
                run.tags.append("16x16") 
        else:
            print("The environment for the run in question was not assignable:")
            print("ID: " + run.id)
            print("Name: " + run.name)
            if run.id in problemsInRun:
                issues = problemsInRun[run.id]
                issues.append(target)
            else:
                problemsInRun[run.id] = [target]
    else:
        print("The environment for the run in question was not assignable:")
        print("ID: " + run.id)
        print("Name: " + run.name)
        if run.id in problemsInRun:
            issues = problemsInRun[run.id]
            issues.append(target)
        else:
            problemsInRun[run.id] = [target]
    return problemsInRun
    
    
def addTimestepTag(run, problemsInRun):
    target = "num_timesteps"
    if target in run.config:
        marker = str(run.config[target])
        run.tags.append(marker)
    else:
        print("The timesteps for the run in question were not assignable:")
        print("ID: " + run.id)
        print("Name: " + run.name)
        if run.id in problemsInRun:
            issues = problemsInRun[run.id]
            issues.append(target)
        else:
            problemsInRun[run.id] = [target]
            
    return problemsInRun
    

def addExtraNoiseTag(run, problemsInRun):
    target = "add_noise"
    if target in run.config:
        marker = run.config[target]
        if marker == "True":
            if "Outside Noise" not in run.tags:
                run.tags.append("Outside Noise")
    return problemsInRun
    
            
def addRandomActionTag(run, problemsInRun):
    target = "random_actions"
    if target in run.config:
        marker = run.config[target]
        if marker == "True":
            if "Random Actions" not in run.tags:
                run.tags.append("Random Actions") 
    return problemsInRun

def addCoverageTag(run, problemsInRun):
    target = "record_coverage"
    if target in run.config:
        marker = run.config[target]
        if marker == "True":
            if "Coverage" not in run.tags:
                run.tags.append("Coverage") 
    return problemsInRun
    
def addActionDependencyTag(run, problemsInRun):
    envRC = "MiniGrid-RandomColours-8x8-v0"
    if "env" in run.config:
        if run.config["env"] == envRC:
            if "rc_dependent" in run.config:
                value = run.config["rc_dependent"]
                typ = type(value)
                if typ == str:
                    if value == "false" or value == "False":
                        value = False
                    else:
                        value = True
                if value:
                    if "AD" not in run.tags:
                        run.tags.append("AD")
                else:
                    if "AI" not in run.tags:
                        run.tags.append("AI")
                        
            if "ra_dependent" in run.config:
                value = run.config["ra_dependent"]
                typ = type(value)
                if typ == str:
                    if value == "false" or value == "False":
                        value = False
                    else:
                        value = True
                if value:
                    if "AD" not in run.tags:
                        run.tags.append("AD")
                else:
                    if "AI" not in run.tags:
                        run.tags.append("AI")
        else:
            if "on_dependent" in run.config:
                value = run.config["on_dependent"]
                typ = type(value)
                if typ == str:
                    if value == "false" or value == "False":
                        value = False
                    else:
                        value = True
                if value:
                    if "AD" not in run.tags:
                        run.tags.append("AD")
                else:
                    if "AI" not in run.tags:
                        run.tags.append("AI")
                         
            if "ra_dependent" in run.config:
                value = run.config["ra_dependent"]
                typ = type(value)
                if typ == str:
                    if value == "false" or value == "False":
                        value = False
                    else:
                        value = True
                if value:
                    if "AD" not in run.tags:
                        run.tags.append("AD")
                else:
                    if "AI" not in run.tags:
                        run.tags.append("AI")

    return problemsInRun

        
    
def addCoverageTag(run, problemsInRun):
    target = "record_coverage"
    if target in run.config:
        marker = run.config[target]
        if marker == "True":
            if "Coverage" not in run.tags:
                run.tags.append("Coverage") 
    return problemsInRun
            
def download_means(runs):
    import os.path
    import glob
    import os
    path = '/home/luki/Documents/thesis/analysis/theNewWorld/the_storage'
    files = [f for f in os.listdir(path) if f.endswith('.json')]
    

    keys = ['Number of Updates', 'Extrinsic Reward (Batch)']
    key = "Batch/Update"
    # key = keysforAvgs[2]

    for run in runs:
        gathering_successed = False
        string = str(run.id) + ".json"
    # if string not in files:
        if run.state == "finished":
            data = run.scan_history(keys = keys)
            values = []
            # gather = 0
            # mean = None
            # counter = 0
            try:
                print("Try processing: " , run.id)

                for row in data:
                    tuple = (row['Number of Updates'],row['Extrinsic Reward (Batch)'])
                    values.append(tuple)
                #     counter += 1
                # mean = gather / counter
                gathering_successed = True
                file_path = "/home/luki/Documents/thesis/analysis/theNewWorld/the_storage/" + string

            except:
                print(run.id, " was not accessible")

            if gathering_successed:
                if os.path.exists(file_path):
                    with open(file_path, "r+") as f:
                        dict = json.load(f)
                        dict[key] = values
                else:
                    dict = {}
                    dict[key] = values

                with open(file_path, "w+") as f:
                    json.dump(dict, f)
                print("Successed.")

            else:
                pass
        else:
            print(run.id, "is still running or crashed!")
        # else:
        #     print("Already downloaded")

if __name__ == '__main__':
    import wandb
    import json
    import pathlib

    wandb.login()
    api = wandb.Api()
    entity, project = "lukischueler", "thesis" 
    path = entity + "/" + project
    runs = api.runs(path)

    # download_means(runs)



    # for run in runs:
    #     print("Processing run")
    #     run.tags = []
    #     run.update()
    # print("DONE")
    
    pathlib.Path('/home/luki/Documents/thesis/analysis/issues').mkdir(parents=True, exist_ok=True) 
    print("Settings are adjusted")
    dataProcessing(runs)
    print("PROCESSING FINSIHED")
