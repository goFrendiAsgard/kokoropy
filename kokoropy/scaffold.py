#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Repo: https://github.com/goFrendiAsgard/kokoropy
'''
__author__  = 'Go Frendi Gunawan'
__version__ = 'development'
__license__ = 'MIT'

from kokoro import *
from copy import copy

def make_timestamp():
    return datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

def write_and_backup(filename, data):
    if os.path.exists(filename):
        old_data = file_get_contents(filename)
        if old_data != data:
            backup_time = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')
            shutil.copy2(filename, filename+'.'+backup_time+'.bak')
    file_put_contents(filename, data)

def scaffold_application(application_name):
    source = os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_application')
    destination = application_path(application_name)
    copytree(source, destination)

def scaffold_migration(application_name, migration_name, table_name='your_table', *columns):
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_migration.py'))
    timestamp = make_timestamp()
    # make timestamp
    content = content.replace('g_timestamp', timestamp)
    # make add column and drop column scripts
    add_column_scripts = []
    drop_column_scripts = []
    for column in columns:
        column = column.split(':')
        if len(column)>1:
            coltype= column[1]
            coltype_element = coltype.split('-')
            if len(coltype_element)>1:
                coltype = coltype_element[0] + '(' + ', '.join(coltype_element[1:]) + ')'
            # in case of string is not defined
            if coltype == 'String':
                coltype = 'String(50)'
            column = column[0]
        else:
            coltype = 'String(50)'
            column = column[0]
        add_column_scripts.append('op.add_column(\'%s\', Column(\'%s\', %s))' % (table_name, column, coltype))
        drop_column_scripts.append('op.drop_column(\'%s\', \'%s\')' % (table_name, column))
    add_column_scripts = '\n    '.join(add_column_scripts)
    drop_column_scripts = '\n    '.join(drop_column_scripts)
    content = content.replace('# g_add_column', add_column_scripts)
    content = content.replace('# g_drop_column', drop_column_scripts)
    # make application if not exists
    if not os.path.exists(application_path(application_name)):
        scaffold_application(application_name)
    # determine file name
    filename = timestamp+'_'+migration_name+'.py'
    filename = application_path(os.path.join(application_name, 'migrations', filename))
    # write file
    write_and_backup(filename, content)

def add_column_to_structure(structure, table_name, column_name = None, content = None, no_form = False):
    '''
    return new column_name
    '''
    if '__list__' not in structure:
        structure['__list__'] = []
    if table_name not in structure:
        structure[table_name] = {'__list__' : []}
        structure['__list__'].append(table_name)
        structure[table_name]['__no_form__'] = no_form
    if column_name is not None:
        if column_name in structure[table_name]:
            i = 1
            while column_name + '_' + str(i) in table_name:
                i += 1
            column_name = column_name + '_' + str(i)
        if content is None:
            content = 'Column(String)'
        structure[table_name][column_name] = content
        structure[table_name]['__list__'].append(column_name)
    return column_name

def add_detail_excluded_shown_column_to_structure(structure, table_name, column_name, detail_column_name):
    if '__detail_excluded_shown_column__' not in structure[table_name]:
        structure[table_name]['__detail_excluded_shown_column__'] = {}
    if column_name not in structure[table_name]['__detail_excluded_shown_column__']:
        structure[table_name]['__detail_excluded_shown_column__'][column_name] = []
    structure[table_name]['__detail_excluded_shown_column__'][column_name].append(detail_column_name)

def add_column_label_to_structure(structure, table_name, column_name, label):
    if '__column_label__' not in structure[table_name]:
        structure[table_name]['__column_label__'] = {}
    structure[table_name]['__column_label__'][column_name] = label

def add_detail_column_label_to_structure(structure, table_name, column_name, detail_column_name, label):
    if '__detail_column_label__' not in structure[table_name]:
        structure[table_name]['__detail_column_label__'] = {}
    if column_name not in structure[table_name]['__detail_column_label__']:
        structure[table_name]['__detail_column_label__'][column_name] = {}
    structure[table_name]['__detail_column_label__'][column_name][detail_column_name] = label

def _structure_to_script(structure, table = None):
    '''
    example of data structure:
        structure = [
            'nerd' = {
                'name' : 'Column(String)',
                'address' : 'Column(String)'
            },
            'os' = {
                'name' : 'Column(String)',
                'version' : 'Column(String)'
            }
        ]
    '''
    if table != None:
        table_list = [table]
        if '__column_label__' in structure[table]:
            for key in structure[table]['__column_label__']:
                table_list.append(key)
    else:
        table_list = structure['__list']
    script = ''
    for table_name in table_list:
        ucase_table_name = table_name.title()
        script += 'class ' + ucase_table_name + '(DB_Model):\n'
        script += '    __session__ = session\n'
        # excluded column
        if '__detail_excluded_shown_column__' in structure[table_name]:
            script += '    # Excluded Columns\n'
            for key in ('__detail_excluded_shown_column__', '__detail_excluded_form_column__'):
                script += '    ' + key + ' = {\n            '
                pair_list = []
                for column_name in structure[table_name]['__detail_excluded_shown_column__']:
                    detail_column_list = structure[table_name]['__detail_excluded_shown_column__'][column_name]
                    new_detail_column_list = []
                    for detail_column in detail_column_list:
                        detail_column = '"' + detail_column + '"'
                        new_detail_column_list.append(detail_column)
                    detail_column_list = new_detail_column_list
                    detail_columns = ', '.join(detail_column_list)
                    pair_list.append('"' + column_name + '" : [' + detail_columns + ']')
                script += ',\n            '.join(pair_list)
                script += '\n        }\n'
        # column's label
        if '__column_label__' in structure[table_name]:
            script += '    # Column\'s Labels\n'
            script += '    __column_label__ = {\n            '
            pair_list = []
            for column_name in structure[table_name]['__column_label__']:
                label = structure[table_name]['__column_label__'][column_name]
                pair_list.append('"' + column_name + '" : "' + label + '"')
            script += ',\n            '.join(pair_list)
            script += '\n        }\n'
        # detail column's label
        if '__detail_column_label__' in structure[table_name]:
            script += '    # Detail Column\'s Labels\n'
            script += '    __detail_column_label__ = {\n            '
            pair_list = []
            for column_name in structure[table_name]['__detail_column_label__']:
                sub_pair_list = []
                for detail_column_name in structure[table_name]['__detail_column_label__'][column_name]:
                    detail_label = structure[table_name]['__detail_column_label__'][column_name][detail_column_name]
                    sub_pair_list.append('"' + detail_column_name + '" : "' + detail_label + '"')
                pair_list.append('"' + column_name + '" : {\n                ' +\
                                 ',\n                '.join(sub_pair_list) + '\n            }')
            script += ',\n            '.join(pair_list)
            script += '\n        }\n'
        script += '    # Fields Declarations\n'
        for column_name in structure[table_name]['__list__']:
            content = structure[table_name][column_name]
            while len(column_name) < 20 :
                column_name += ' '
            script += '    ' + column_name + ' = ' + content + '\n'
        script += '\n'
    return script

def _scaffold_model(structure, table_name, *columns):
    ucase_table_name = table_name.title()
    for column in columns:
        column = column.split(':')
        if len(column)>2:
            colname = column[0]
            other_table_name = column[1]
            relationship = column[2]
            ucase_other_table_name = other_table_name.title()
            if relationship == 'onetomany' or relationship == 'one_to_many' or relationship == 'one-to-many':
                # other table
                add_column_to_structure(structure, other_table_name)
                # foreign key
                coltype = 'Column(Integer, ForeignKey("' + table_name + '._real_id"))'
                fk_col_name = 'fk_' + table_name
                fk_col_name = add_column_to_structure(structure, other_table_name, fk_col_name, coltype)
                # relationship
                coltype = 'relationship("' + ucase_other_table_name + '", foreign_keys="' + ucase_other_table_name + '.' + fk_col_name + '")'
                add_column_to_structure(structure, table_name, colname, coltype)
            elif relationship == 'manytoone' or relationship == 'manytone' or relationship == 'many_to_one' or relationship == 'many-to-one':
                # other table
                add_column_to_structure(structure, other_table_name)
                # foreign key
                coltype = 'Column(Integer, ForeignKey("' + other_table_name + '._real_id"))'
                fk_col_name = 'fk_' + colname
                fk_col_name = add_column_to_structure(structure, table_name, fk_col_name, coltype)
                # relationship
                coltype = 'relationship("' + ucase_other_table_name + '", foreign_keys="' + ucase_table_name + '.' + fk_col_name + '")'
                add_column_to_structure(structure, table_name, colname, coltype)
            elif relationship == 'manytomany' or relationship == 'many_to_many' or relationship == 'many-to-many':
                # other table
                add_column_to_structure(structure, other_table_name)
                # association table
                association_table_name = table_name + '_' + colname
                ucase_association_table_name = association_table_name.title()
                add_column_to_structure(structure, association_table_name, None, None, True)
                # determine foreign key & relationship names
                if table_name == other_table_name:
                    fk_col_name_left = 'fk_left_' + table_name
                    fk_col_name_right = 'fk_right_' + other_table_name
                    rel_col_name_left = 'left_' + table_name
                    rel_col_name_right = 'right_' + other_table_name
                else:
                    fk_col_name_left = 'fk_' + table_name
                    fk_col_name_right = 'fk_' + other_table_name
                    rel_col_name_left = table_name
                    rel_col_name_right = other_table_name
                rel_col_name = table_name + '_' + colname
                # foreign key 1 (to this table)
                coltype = 'Column(Integer, ForeignKey("' + table_name + '._real_id"))'
                fk_col_name_left = add_column_to_structure(structure, association_table_name, 
                    fk_col_name_left, coltype)
                # foreign key 2 (to other table)
                coltype = 'Column(Integer, ForeignKey("' + other_table_name + '._real_id"))'
                fk_col_name_right = add_column_to_structure(structure, association_table_name, 
                    fk_col_name_right, coltype)
                # relationship (from association table to table)
                coltype = 'relationship("' + ucase_table_name + '",' +\
                    ' foreign_keys="' + ucase_association_table_name + '.' + fk_col_name_left + '")'
                rel_col_name_left = add_column_to_structure(structure, association_table_name, 
                    rel_col_name_left, coltype)
                # relationship (from association table to other table)
                coltype = 'relationship("' + ucase_other_table_name + '",' +\
                    ' foreign_keys="' + ucase_association_table_name + '.' + fk_col_name_right + '")'
                rel_col_name_right = add_column_to_structure(structure, association_table_name, 
                    rel_col_name_right, coltype)
                # relationship (from table to association table)
                coltype = 'relationship("' + ucase_association_table_name + '",' +\
                    ' foreign_keys="' + ucase_association_table_name + '.' + fk_col_name_left + '")'
                rel_col_name = add_column_to_structure(structure, table_name, rel_col_name, coltype)
                # proxy
                coltype = 'association_proxy("' + rel_col_name + '", "' + fk_col_name_right + '",'+\
                    ' creator = lambda _val : ' + ucase_association_table_name +\
                    '(' + rel_col_name_right + ' = _val))'
                add_column_to_structure(structure, table_name, colname, coltype)
                # add detail excluded shown column
                add_detail_excluded_shown_column_to_structure(structure, table_name, 
                    rel_col_name, rel_col_name_left)
                # add column label to structure
                add_column_label_to_structure(structure, table_name, rel_col_name, colname.replace('_', ' ').title())
                # add detail column label to structure
                if table_name == other_table_name:
                    add_detail_column_label_to_structure(structure, table_name, rel_col_name, 
                        rel_col_name_right, ucase_table_name.replace('_', ' '))
        else:
            colname = column[0]
            if len(column)>1:
                coltype = column[1]
                coltype_element = coltype.split('-')
                if len(coltype_element)>1:
                    coltype = coltype_element[0] + '(' + ', '.join(coltype_element[1:]) + ')'
                # in case of length is not defined
                if coltype == 'String':
                    coltype = 'String(50)'
            else:
                coltype = 'String(50)'
            add_column_to_structure(structure, table_name, colname, 'Column('+coltype+')')

def scaffold_model(application_name, table_name, *columns):
    structure = {'__list__' : []}
    # prototype_structure
    table_list = [table_name]
    column_list = {table_name : []}
    table = table_name
    new_table = False
    for i in xrange(len(columns)):
        column = columns[i]
        if new_table:
            new_table = False
            table = column
            table_list.append(table)
            column_list[table] = []
            continue
        if column[-1] == ',':
            new_table = True
            if column != ',':
                column = column[:-1]
            else:
                continue
        column_list[table].append(column)
    # make application if not exists
    if not os.path.exists(application_path(application_name)):
        scaffold_application(application_name)
    # add prototype_structure
    for table in table_list:
        # define structure
        table_column_list = column_list[table]
        _scaffold_model(structure, table, *table_column_list)
    import_str = ''
    for table in table_list:
        content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_model.py'))
        # replace content
        content = content.replace('# g_structure', _structure_to_script(structure, table))        
        # determine file name
        filename = table+'.py'
        filename = application_path(os.path.join(application_name, 'models', filename))        
        # write file
        write_and_backup(filename, content)
        # assembly import
        class_list = [table.title()]
        if '__column_label__' in structure[table]:
            for key in structure[table]['__column_label__']:
                class_list.append(key.title())
        import_str += 'from ' + table + ' import ' + ', '.join(class_list) + '\n'
    # create _structure
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_structure.py'))
    # replace content
    content = content.replace('# g_import', import_str)
    filename = application_path(os.path.join(application_name, 'models', '_structure.py'))        
    # write file
    write_and_backup(filename, content)
    return structure

def scaffold_crud(application_name, table_name, *columns):
    structure = scaffold_model(application_name, table_name, *columns)
    ucase_table_name_list = []
    for t in structure:
        if t == '__list__':
            continue
        ucase_table_name_list.append(t.title())
    ucase_table_name_list = ", ".join(ucase_table_name_list)
    
    controller_filename = application_path(os.path.join(application_name, 'controllers', 'index.py'))
    url_pairs = []
    for t in structure['__list__']:
        if structure[t]['__no_form__']:
            continue
        url_pairs.append('\'%s\' : base_url(\'%s/%s\')' %(t.replace('_',' ').title(), application_name, t))
    url_pairs = ',\n            '.join(url_pairs)
    # main controller
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_main_controller.py'))
    content = content.replace('# g_url_pairs', url_pairs)
    content = content.replace('g_application_name', application_name)
    write_and_backup(controller_filename, content)
    # main view
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_main_view.html'))
    content = content.replace('g_application_name', application_name)
    filename = application_path(os.path.join(application_name, 'views', 'index.html'))
    write_and_backup(filename, content)
    
    # for each table, make controller and views
    for table_name in structure['__list__']:
        # don't make controller and views for association table
        if structure[table_name]['__no_form__']:
            continue
        ucase_table_name = table_name.title()
        # controller
        content = file_get_contents(os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_controller.py'))
        content = content.replace('G_Table_Name', ucase_table_name)
        content = content.replace('g_table_name', table_name)
        content = content.replace('g_application_name', application_name)
        filename = table_name+'.py'
        filename = application_path(os.path.join(application_name, 'controllers', filename))
        # write file
        write_and_backup(filename, content)
        # views
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'remove', 'delete', 'destroy']
        view_directory = application_path(os.path.join(application_name, 'views', table_name))
        if not os.path.isdir(view_directory):
            makedirs(view_directory)
        # make readme
        content = 'You can make your own custom file by providing : \n'
        for view in view_list:
            content += '* %s.html\n' %(view)
        write_and_backup(os.path.join(view_directory, '_README.txt'), content)

def scaffold_view(application_name, table_name, view = None):
    view_directory = application_path(os.path.join(application_name, 'views', table_name))
    ucase_table_name = table_name.title()
    if not os.path.isdir(view_directory):
        makedirs(view_directory)
    if view is not None:
        view_list = [view]
    else:
        view_list = ['list', 'show', 'new', 'create', 'edit', 'update', 'trash', 'remove', 'delete', 'destroy', 'search']
    for view in view_list:
        content = file_get_contents(os.path.join(os.path.dirname(__file__), 'views', view + '.html'))
        content = content.replace('G_Table_Name', ucase_table_name)
        content = content.replace('g_table_name', table_name)
        content = content.replace('g_application_name', application_name)
        filename = view + '.html'
        filename = os.path.join(view_directory, filename)
        # write file
        write_and_backup(filename, content)

def scaffold_cms():
    source = os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_cms')
    destination = application_path('cms')
    copytree(source, destination)


def scaffold_project(project_name):
    source = os.path.join(os.path.dirname(__file__), 'scaffolding', 'scaffold_application')
    destination = os.path.join(os.getcwd, project_name)
    copytree(source, destination)
    # copy rossian.py
    source_dir = os.path.dirname(os.path.dirname(__file__))
    shutil.copyfile(os.path.join(source_dir, 'rossian.py'), os.path.join(destination, 'rossian.py'))