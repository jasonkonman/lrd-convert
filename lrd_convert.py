import streamlit as st
import pandas as pd
import numpy as np
import json


def main():

    ### Title
    st.title("LRD Config Generator")

    ### Section 1: Upload source file
    with st.container() as container_1:
        st.header("Step 1: Upload File")
        with st.form(key='upload_xlsx'):
            input_file = st.file_uploader("Upload excel file here", type=['xlsx'], key='dirty_file')
            submit_button = st.form_submit_button(label='Generate LRD Config')
    

    ### Checking if file is valid
    if submit_button:
        try:
            st.success(f"{input_file.name} has been uploaded\n\n")
            st.text("")
            st.markdown("***")
            st.header("\n\nStep 2: Check Data")
            if input_file is None:
                pass
            else:
                df_q = pd.read_excel(input_file, sheet_name='questionnaire')
                df_c = pd.read_excel(input_file, sheet_name='columns')
                df_t = pd.read_excel(input_file, sheet_name='thresholds')

                df_t = df_t[df_t['tableheader'].notnull()]
                df_c = df_c[df_c['tableheader'].notnull()]

    
            ### Put output json together
            out = {}
            out['questionnaireId'] = df_q.loc[0,'questionnaireid']
            out['hideColumns'] = df_q[df_q['hidecolumns'].notnull()]['hidecolumns'].to_list()
            out['columns'] = []

            # Table columns
            for index, row in df_c.iterrows():
                j_row = {}
                j_row['title'] = row['tableheader']
                j_row['variableType'] = row['variabletype']
                j_row['valueType'] = row['valuetype']
                if row['valuetype'] == 'string':
                    j_row['precision'] = 0
                else:
                    j_row['precision'] = int(row['precision'])
                    
                j_row['id'] = []
                j_row['id'].append(row['questionid'])
                j_row['thresholds'] = []
                out['columns'].append(j_row)

            # Thresholds
            for index, row in df_t.iterrows():
                t_row = {}
            
                if row['valuetype'] == 'string':
                    t_row['value'] = str(row['value'])
                    
                elif row['valuetype'] == 'number':
                    if row['min'] == 'null':
                        t_row['min'] = None
                    else:
                        t_row['min'] = float(row['min'])
                    
                    if row['max'] == 'null':
                        t_row['max'] = None
                    else:
                        t_row['max'] = float(row['max'])
                
                else:
                    pass
                
                t_row['type'] = row['type']
                
                # conditionally append threshold to threshold array
                for item in out['columns']:
                    if item['title'] == row['tableheader']:
                        item['thresholds'].append(t_row)
                    else:
                        pass

            ### OUTPUT df container
            container_output = st.container()
            container_output.text("")
            container_output.subheader("LRD Config")
            # container_output.write(json.dumps(out, ensure_ascii=False, indent=4).replace(": NaN,", ": null,"))
            st.code(json.dumps(out, ensure_ascii=False, indent=4).replace(": NaN,", ": null,"), language='json')

        except AttributeError:
            st.error("Please select a file before continuing")

if __name__ == '__main__':
    main()
