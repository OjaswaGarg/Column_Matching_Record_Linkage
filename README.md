# Column_Matching_Record_Linkage
## Collaborators
### [Ojaswa Garg](https://github.com/OjaswaGarg)
### [Adhiraj Srivastava](https://github.com/adhirajms)
### [Vijay Nallapaneni](https://github.com/vij95)

Our goal via this repository is to provide a way for people to preprocess data so that it can be used against our record linkage models.
The record linkage models can be accessed with the help of below links-
https://github.com/OjaswaGarg/Flask_Record_Linkage
https://recordlinkage.azurewebsites.net/
https://bit.ly/record_linkage

Through our project we wanted to provide a pipeline which helps in matching records while ensuring that privacy of the individuals is protected. The project focuses on finding an efficient approach to perform record linkage. Given two datasets which contain records, the record-linkage problem consists of determining all pairs that are similar to each other.


## How to run
- Run the command  ``` pip3 install -r install.txt ``` to install all the dependencies (Python 3).
  One can also create a conda environment with the help of the record linkage yml file ``` conda env create -f record_linkage.yml ```

- The script, ```Column_Matching_Components.py``` is the final script. The datasets are already provided. 
- Sample way to run the script via terminal is using the command ```Column_Matching_Components.py```
