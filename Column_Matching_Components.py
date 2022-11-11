#Importing libraries
# %%
import re 
import pandas as pd
import sys
import pickle
import dataprofiler as dp
import warnings
warnings.filterwarnings('ignore')
import time
from encryption import encryption_func


my_dict= {'name': 'First Name', 'givenname': 'First Name', 'fname': 'First Name', 'firstname': 'First Name', 'first': 'First Name',
          'surname': 'Last Name', 'familyname': 'Last Name', 'lname': 'Last Name', 'lastname': 'Last Name', 'last': 'Last Name',
          'streetno': 'Street Number', 'stno': 'Street Number', 'streetnumber': 'Street Number',
          'streetaddress': 'Address1', 'addr': 'Address1', 'addressline1': 'Address1', 'address':'Address1', 'address1':'Address1',
          'unitnumber': 'Address2', 'apartmentnumber': 'Address2', 'addr2': 'Address2', 'addressline2': 'Address2', 'address2': 'Address2',
          'county': 'Suburb', 'city': 'Suburb', 'area': 'Suburb', 'region': 'Suburb', 'suburb':'Suburb',
          'zipcode':'Postcode', 'areacode':'Postcode','zip':'Postcode', 'postalcode':'Postcode', 'postcode':'Postcode',
          'state': 'State',
          'dob':'Date of Birth', 'birthdate':'Date of Birth', 'dateofbirthddmmyy':'Date of Birth', 'dateofbirthmmddyy':'Date of Birth', 'dateofbirthddmmyyyy':'Date of Birth', 'dateofbirthmmddyyyy':'Date of Birth', 'dobddmmyy':'Date of Birth', 'dobmmddyy':'Date of Birth', 'dobddmmyyyy':'Date of Birth', 'dobmmddyyyy':'Date of Birth', 'dateofbirth':'Date of Birth',
          'ssn':'Social Security Number', 'socsecid': 'Social Security Number', 'socialsecuritynumber':'Social Security Number', 'ssa':'Social Security Number', 'socialsecuritycard':'Social Security Number', 'ssid':'Social Security Number', 'socialsecuritynumer':'Social Security Number',
          'contactnumber':'Phone Number', 'number':'Phone Number', 'phone':'Phone Number', 'phno':'Phone Number', 'phoneo':'Phone Number', 'phnumber':'Phone Number', 'mobile':'Phone Number', 'mobileno':'Phone Number', 'mobilenumber':'Phone Number', 'cellphone':'Phone Number', 'cellphoneno':'Phone Number', 'cellphonenumber':'Phone Number', 'phonenumber':'Phone Number',
          'email':'Email Address', 'emailid':'Email Address', 'emailaddress':'Email Address'}

def column_dictionary_match (df_list):
    canonical_list=[]
    def standard_name(col_name):
        col_name= ''.join(col_name.split()).lower()
        col_name= re.sub("[^A-Za-z0-9]", '', col_name)
        if col_name in list(my_dict.keys()):
            col_name=my_dict[col_name]
        else:
            canonical_list[-1].append(col_name)    
        return col_name

    for ind,df in enumerate(df_list):
        canonical_list.append([])
        df.rename(columns=lambda x: standard_name(x), inplace=True)
    return df_list,canonical_list






def data_profiler (df, canonical_lst):
    # set options to only run the labeler
    profile_options = dp.ProfilerOptions()
    profile_options.set({"structured_options.text.is_enabled": False, 
                        "int.is_enabled": False, 
                        "float.is_enabled": False, 
                        "order.is_enabled": False, 
                        "category.is_enabled": False, 
                        "chi2_homogeneity.is_enabled": False,
                        "datetime.is_enabled": False,})


    # helper functions for printing results

    def get_structured_results(results):
        """Helper function to get data labels for each column."""
        columns = []
        predictions = []
        samples = []
        for col in results['data_stats']:
            columns.append(col['column_name'])
            predictions.append(col['data_label'])
            samples.append(col['samples'])

        df_results = pd.DataFrame({'Column': columns, 'Prediction': predictions, 'Sample': samples})
        return df_results

    def get_unstructured_results(data, results):
        """Helper function to get data labels for each labeled piece of text."""
        labeled_data = []
        for pred in results['pred'][0]:
            labeled_data.append([data[0][pred[0]:pred[1]], pred[2]])
        label_df = pd.DataFrame(labeled_data, columns=['Text', 'Labels'])
        return label_df

    def check_data (dataframe, labeler):
        profile_options.set({'structured_options.data_labeler.data_labeler_object': labeler})
        profile = dp.Profiler(dataframe, options=profile_options)
        # get the prediction from the data profiler
        results = profile.report()
        return(get_structured_results(results))


    
    #ACTUAL MATCHING
    
    data_labeler = pickle.load(open('data_labeler.pickle', 'rb'))
    a=check_data(df[canonical_lst], data_labeler)
    columns_used=[i for i in list(df.columns) if i not in canonical_lst]
    my_dict2={}
    print(columns_used)
    print(a)
    for index, row in a.iterrows():
        options=row['Prediction']
        options_list=options.split('|')
        options_list=[i for i in options_list if i not in columns_used]
        row['Prediction']="|".join(options_list)
        while options_list:
            print('Column:',row['Column'],'Prediction:',options_list[0],'Sample:',row['Sample'])
            time.sleep(1)
            x = input('Is this a match '+row['Column']+'--'+options_list[0]+ '(y/n)?')
            if (x == 'y' or x=='Y'):
                my_dict2[row['Column']]=options_list[0]
                columns_used.append(options_list[0])
                break
            else:
                options_list.pop(0)
    df.rename(columns=lambda x: my_dict2[x] if x in list (my_dict2.keys()) else x, inplace=True)
    return df



#CUSTOM MATCHING

def custom_matching (df):
    my_dict3={}
    x = input('Do you want to do custom matching (y/n)?')
    if x!='y' and x!='Y':
        return df
    columns_model=["First Name","Last Name","Suburb","State","Address","Date of Birth"]
    missing_cols = [ i for i in columns_model if i not in list(df.columns)]
    perspective_cols=[i for i in list(df.columns) if i not in columns_model]
    for i in perspective_cols:
        if not missing_cols:
            continue
        options="\n"
        for ind,col in enumerate(missing_cols):
            options+=col+" -> "+str(ind)+"\n"
        options+=" None -> -1"+"\n"
        x = input('Match the column '+i+' with the help of options'+options) 
        try:
            x=int(x)
        except:
            x=-1
        if x>=0 and x<len(missing_cols):
            my_dict3[i]=missing_cols[x]
            missing_cols.pop(x)
    df.rename(columns=lambda x: my_dict3[x] if x in list (my_dict3.keys()) else x, inplace=True)
    return df

if __name__ == "__main__":
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[2])
    outputh_path=sys.argv[3]
    list1=sys.argv[1].split('/')
    output_file=outputh_path+"/output"
    df_list,canonical_list=column_dictionary_match([df1,df2])
    for i in range (len(df_list)):
        print('*******************Working on Data '+str(i+1)+' *********************')
        x = input('Is data '+str(i+1)+' encrypted? Type Y/N ') 
        if x!='y' and x!='Y':
            df_list[i]=data_profiler(df_list[i],canonical_list[i])
            df_list[i]=encryption_func(df_list[i])
        df_list[i]=custom_matching(df_list[i])    
        df_list[i] = df_list[i].astype(str)
        df_list[i].to_csv(output_file+str(i+1)+'.csv',index=False)
        print("--------------------------------Finish "+str(i+1)+" ----------------------\n"+output_file+str(i+1)+'.csv')





# %%
