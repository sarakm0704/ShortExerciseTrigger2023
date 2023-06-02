# Trigger Short Exercise 2023
Trigger short exercise CMS DAS @ CERN, June 2023

See DAS twiki for detailed instructions:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolCERN2023TriggerExercise

## Jupyter noteboooks

If you want to use Jupyter notebooks on lxplus, please review the content of your `~/.ssh/config` file on your system by executing:

    cat ~/.ssh/config

In case the file does already contain the following lines, add:

    Host lxplus*.cern.ch
        StrictHostKeyChecking no
        UserKnownHostsFile /dev/null

When you log into cmslpc, add a `-L` option to your ssh command:

    ssh -L localhost:8888:localhost:8888 <YOUR USERNAME>@lxplus.cern.ch

Then you can make your area

```    
source /cvmfs/cms.cern.ch/cmsset_default.csh
cd nobackup/
mkdir -p CMSDAS2023/Trigger
cd CMSDAS2023/Trigger
cmsrel CMSSW_12_6_4
cd CMSSW_12_6_4/src
cmsenv
git clone https://github.com/marinakolosova/ShortExerciseTrigger2023.git
scram b -j 4
cd ShortExerciseTrigger2023/ShortExerciseTrigger
```

And start Jupyter with this command:

    jupyter notebook --no-browser --port=8888

After a pause (while lxplus loads the necessary libraries for the first time) you should see a message like the following:

    [I 11:30:05.670 NotebookApp] Serving notebooks from local directory: /afs/cern.ch/work/X/XXXX/cmsdas2023/nobackup/CMSDAS2023/Trigger/CMSSW_12_6_4/src
    [I 11:30:05.671 NotebookApp] Jupyter Notebook 6.4.12 is running at:
    [I 11:30:05.671 NotebookApp] http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    [I 11:30:05.671 NotebookApp]  or http://127.0.0.1:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    [I 11:30:05.671 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [C 11:30:05.703 NotebookApp] 
    
        To access the notebook, open this file in a browser:
            file:///afs/cern.ch/user/X/XXXX/.local/share/jupyter/runtime/nbserver-XXXXX-open.html
        Or copy and paste one of these URLs:
            http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        or http://127.0.0.1:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
