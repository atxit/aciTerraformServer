
df_tf = build()


df_tf = df_tf.loc[~df_tf['resourceId'].str.match('N/A')].copy()
df_deps = df_tf.loc[df_tf['resourceValue'].str.contains(r'.id$')].copy()
for resource_type in df_deps['resourceType']:
    df_tf = df_tf.loc[~df_tf['resourceType'].str.match(resource_type)].copy()


df_root = df_tf[['resourceId']].drop_duplicates().copy()
df_deps = df_deps[['resourceId','resourceValue']].copy()


column_ref = 0

df_root.rename(columns={'resourceId': column_ref}, inplace=True)
df_deps.rename(columns={'resourceValue': column_ref}, inplace=True)
df_root = df_root.merge(df_deps, left_on=column_ref, right_on=column_ref, how='inner')
df_root.rename(columns={'resourceId': column_ref+1}, inplace=True)
df_deps.rename(columns={column_ref: column_ref+1}, inplace=True)

#df_root.drop(columns=['resourceValue'], inplace=True)

column_ref += 1
#df_root.rename(columns={'resourceId': column_ref}, inplace=True)


continue_processing = True

while continue_processing:
    current_shape = df_root.shape
    df_root = df_root.merge(df_deps, left_on=column_ref, right_on=column_ref, how='outer').dropna(subset=[column_ref-1])
    df_root.rename(columns={'resourceId': column_ref+1}, inplace=True)
    df_deps.rename(columns={column_ref: column_ref+1}, inplace=True)
    df_root.dropna(how='all', axis=1, inplace=True)
    df_root.fillna('', inplace=True)
    column_ref += 1
    if current_shape == df_root.shape:
        continue_processing = False



def located_searched_item(df_root, resource_lookup):
    df_results = pd.DataFrame()
    remove_list = []
    searching = True
    for column_id in df_root.columns:
        df_column = df_root.loc[df_root[column_id].str.contains(resource_lookup)].copy()
        if len(df_column) == 0 and searching:
            remove_list.append(column_id)
        else:
            searching = False
            df_results = pd.concat([df_results,df_column])
    df_results = df_results.replace('',np.nan).dropna(axis=1).fillna('')
    df_results.index = np.arange(1, len(df_results) + 1)
    return df_results


def remove_all_but_one_references_in_column(df_results):
    single_ref_list = []
    for column_head in df_results.columns:
        column_heads = list(set(df_results[column_head]))
        if len(column_heads) == 1:
            for enumerate_i, results_index in enumerate(df_results.index):
                if enumerate_i != 0:
                    df_results.loc[results_index, 0] = np.nan
            single_ref_list.append(column_head)
    df_results.sort_index(inplace=True)
    return df_results, single_ref_list



def prepare_table_for_markmap(df_results,single_ref_list):
    result_heads = [x for x in df_results.columns.tolist() if x not in single_ref_list]
    df_results.sort_values(by=result_heads, inplace=True)
    df_mark_map = pd.DataFrame()
    if len(result_heads) > 0:
        for result_heads_idx in list(dict.fromkeys(df_results[result_heads[0]])):
            df_slice = df_results.loc[df_results[result_heads[0]].str.match(result_heads_idx)].copy()
            for column_idx in df_slice.columns:
                sliced_column_list = list(set(df_slice[column_idx]))
                for i in df_slice.index:
                    if df_slice.at[i, column_idx] in sliced_column_list:
                        sliced_column_list.remove(df_slice.at[i, column_idx])
                    else:
                        df_slice.loc[i, column_idx] = np.nan
            df_mark_map = pd.concat([df_mark_map,df_slice])
        for i in single_ref_list:
            df_mark_map[i] = df_mark_map[i].ffill().bfill()
        df_mark_map.index = np.arange(1, len(df_mark_map) + 1)
        for single_ref in single_ref_list:
            for markmap_index in df_mark_map.index:
                if markmap_index != 1:
                    df_mark_map.loc[markmap_index,single_ref] = ''
        df_mark_map.fillna('', inplace=True)
        return df_mark_map
    return df_results


def create_markmap_input(df_markmap,resource_lookup):
    markmap_str = ''
    for i in df_markmap.index:
        for enumerate_idx, element in enumerate(df_markmap.loc[i].values.tolist(),1):
            if len(element) > 0:
                if element == resource_lookup:
                    element = '=='+element+'=='
                markmap_str += f'{enumerate_idx*"#"} {element}\n'
    return markmap_str


resource_lookup = 'aci_vrf.demo-VRF.id'
resource_lookup = 'aci_epg_to_static_path.path-129-1-3-999-r.id'
resource_lookup = 'aci_application_epg.demo-app.id'
resource_lookup = 'aci_l3_domain_profile.demo-l3-profile.id'

df_results = located_searched_item(df_root, resource_lookup)
df_results, single_ref_list = remove_all_but_one_references_in_column(df_results)
df_markmap = prepare_table_for_markmap(df_results, single_ref_list)
markmap_str = create_markmap_input(df_markmap,resource_lookup)
print(markmap_str)




column_id = 2
test = list(set(df_results[2]))

for i in df_results.index:
    if df_results.at[i, 2] in test:
        test.remove(df_results.at[i, 2])
    else:
        df_results.loc[i, 2] = ''

column_id = 3
test = list(set(df_results[3]))

for i in df_results.index:
    if df_results.at[i, 3] in test:
        test.remove(df_results.at[i, 3])
    else:
        df_results.loc[i, 3] = ''

column_id = 4
test = list(set(df_results[4]))

for i in df_results.index:
    if df_results.at[i, 4] in test:
        test.remove(df_results.at[i, 4])
    else:
        df_results.loc[i, 4] = ''


column_id = 5
test = list(set(df_results[5]))

for i in df_results.index:
    if df_results.at[i, 5] in test:
        test.remove(df_results.at[i, 5])
    else:
        df_results.loc[i, 5] = ''








used_dict = {}
test = '# root\n'
test = ''
for i in df_results.index:
    #test_a = list(filter(None, df_results.loc[i].values.tolist()))
    test_a = df_results.loc[i].values.tolist()
    #test_a.reverse()
    for x, e in enumerate(test_a,1):
        if x not in used_dict:
            used_dict[x] = [e]
            if e == resource_lookup:
                e = '=='+e+'=='
            test += f'{x*"#"} {e}\n'
        elif e not in used_dict[x]:
            used_dict[x].append(e)
            print(used_dict)
        if e == resource_lookup:
            e = '=='+e+'=='
        test += f'{x*"#"} {e}\n'






test = list(df_root.columns)
test.reverse()




df_root.drop(columns=remove_list, inplace=True)

list(df_results.columns)


for x, column_id in enumerate(df_root.columns):
    df_root.rename(columns={column_id: x}, inplace=True)

main_column_list = list(df_root.columns)

for column_id in df_root.columns:
    df_column = df_root.loc[df_root[column_id].str.contains(resource_lookup)].copy()
    if len(df_column) > 0:
        df_column = df_column.loc[column_id:].copy()
        print(df_column)
        break

        for x, ttt in enumerate(df_column.columns):
            df_column.rename(columns={ttt: x}, inplace=True)
        df_results = pd.concat([df_results,df_column])


df_results.index = np.arange(1, len(df_results) + 1)

removed_list = []

for column_id in df_results.columns:
    print(list(df_results[column_id]))
    print(list(df_results[column_id]).count(resource_lookup))
    print(len(df_results))
    print(list(df_results[column_id]))
    if list(df_results[column_id]).count(resource_lookup) == 0:
        print('all')
        for row_id in df_results.index:
            if row_id not in removed_list:
                df_results.loc[row_id, column_id] = ''
    else:
        for row_id in df_results.index:
            if row_id not in removed_list and df_results.at[row_id, column_id] != resource_lookup and row_id not in removed_list:
                df_results.loc[row_id, column_id] = ''
                removed_list.append(row_id)
    print(removed_list)


for i, column_id in enumerate(df_results.columns):
    for row_id in df_results.index:
        if df_results.at[row_id, column_id] == '':
            try:
                df_results.loc[row_id, column_id] = df_results.at[row_id,column_id.replace(f':{i}',f':{i+1}')]
            except:
                pass

used_dict = {}

test = ''
for i in df_results.index:
    test_a = list(filter(None, df_results.loc[i].values.tolist()))
    #test_a.reverse()
    for x, e in enumerate(test_a,1):
        if x not in used_dict:
            used_dict[x] = [e]
            test += f'{x*"#"} {e}\n'
        elif e not in used_dict[x]:
            used_dict[x].append(e)
            print(used_dict)
            test += f'{x*"#"} {e}\n'




#####

df_tf = build()

column_ref = 0
df_tf = df_tf.loc[~df_tf['resourceId'].str.match('N/A')].copy()
resource_id = 'aci_tenant.demo-test.id'
df_search = df_tf.loc[df_tf['resourceId'].str.contains(resource_id)].copy()
df_search.drop_duplicates(subset=['resourceId'], inplace=True)
df_search = df_search[['resourceId']].copy()
df_search.rename(columns={'resourceId': column_ref}, inplace=True)
df_deps = df_tf.loc[df_tf['resourceValue'].str.contains(r'.id$')].copy()
df_deps = df_deps[['resourceId','resourceValue']].copy()
df_search = df_search.merge(df_deps, left_on=column_ref, right_on='resourceValue', how='inner').drop(columns=['resourceValue']).rename(columns={'resourceId': column_ref})


for resource_type in df_deps['resourceType']:
    df_tf = df_tf.loc[~df_tf['resourceType'].str.match(resource_type)].copy()



df_root = df_tf[['resourceId']].drop_duplicates().copy()
df_deps = df_deps[['resourceId','resourceValue']].copy()


df_slice = df_root.loc[df_root['resourceId'].str.match('aci_tenant.demo-test.id')].copy()
df_root = df_slice.merge(df_deps, left_on=f'resourceId', right_on='resourceValue', how='inner')

column_ref = 0
df_root.rename(columns={'resourceId': f'resourceId:{column_ref}'}, inplace=True)
#df_root =
df_root = df_root.merge(df_deps, left_on=f'resourceId:{column_ref}', right_on='resourceValue', how='inner')
df_root.drop(columns=['resourceValue'], inplace=True)
column_ref += 1
df_root.rename(columns={'resourceId': f'resourceId:{column_ref}'}, inplace=True)

continue_processing = True


while continue_processing:
    current_shape = df_root.shape
    df_root = df_root.merge(df_deps, left_on=f'resourceId:{column_ref}', right_on='resourceValue', how='outer').dropna(subset=[f'resourceId:{column_ref}'])
    df_root.drop(columns=['resourceValue'], inplace=True)
    column_ref += 1
    df_root.rename(columns={'resourceId': f'resourceId:{column_ref}'}, inplace=True)
    df_root.dropna(how='all', axis=1, inplace=True)
    df_root.fillna('', inplace=True)
    if current_shape == df_root.shape:
        continue_processing = False



