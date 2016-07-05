from __future__ import print_function


import Autodesk.Revit.DB as rvt_db
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory 
from Autodesk.Revit.DB import FamilyInstance, FamilySymbol
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import Line, XYZ, CurveLoop




import System
import inspect


import logging
#from adodbapi.schema_table import names

#FilteredElementCollector, BuiltInCategory, View

#uidoc = __revit__.ActiveUIDocument
#doc = __revit__.ActiveUIDocument.Document

# NOTES ----
"""

#A legend:
# this_elem = util_ra.get_element_from_id(rvt_doc, 4703098)
# print(this_elem.ViewType)
# 
# #A view:
# this_elem = util_ra.get_element_from_id(rvt_doc, 5035828)
# print(this_elem.ViewType)

# Get all floorplans, sheets, titleblocks, legends---




#     for v in floorplans:
#         phasep = v.LookupParameter('Phase')
#         sheetnum = v.LookupParameter('Sheet Number')
#         detnum = v.LookupParameter('Detail Number')
#         refsheet = v.LookupParameter('Referencing Sheet')
#         refviewport = v.LookupParameter('Referencing Detail')
# 
#         print('TYPE: {1}ID: {2}PHASE:{4}  {0}'.format(
#                 v.ViewName,
#                 str( v.ViewType ).ljust(20),
#                 str(v.Id).ljust(10),
#                 str(v.IsTemplate).ljust(10),
#                 phasep.AsValueString().ljust(25) if phasep else '---'.ljust(25),
#             ))
"""
 
#-Utility---
def get_self():
    return inspect.stack()[1][3]

class Trans():
    def __init__(self, doc, msg):
        self.msg = msg
        self.t = Transaction(doc, msg)
        
    def __enter__(self):
        logging.debug("TRANSACTION INITATIATED - {}".format(self.msg))
        self.t.Start()
    
    def __exit__(self, exception_type, exception_value, traceback):
        logging.debug("TRANSACTION COMPLETE - {}".format(self.msg))
        self.t.Commit()
        

#-Family---

def get_type(this_elem):
    raise
    this_elem.GetType() # For floorplans!

def get_all_categories(doc):
    categories = doc.Settings.Categories;
    print("{:40} | {:30} | {:30}".format("cat.Name", "cat.Id", "cat.Parent"))    
    for cat in categories:
        print("{:40} | {:30} | {:30}".format(cat.Name, cat.Id, cat.Parent))

def get_all_BuiltInCategory():
    raise
    builtIn = System.Enum.ToObject(BuiltInCategory)
    
#     for bic in BuiltInCategory.GetValue():
#         print(bic)


def get_elements(doc,category):
    #category = BuiltInCategory.OST_Mass
    
    collector = FilteredElementCollector(doc)
    collector.OfCategory(category)
    return collector


def get_table(path_excel_book):
    
    end_row = 4
    
    with util_excel.ExtendedExcelBookAPI(path_excel_book) as xl:
        print(xl)
        table = xl.get_table_2("REGISTER",2,end_row,1,40)
    
    headers = table.pop(0)
    data = table
    
    data_table = list()
    for row in data:
        data_table.append(dict(zip(headers, row)))
        
    logging.info("Got {} rows from {}".format(len(data_table),path_excel_book))
    
    return data_table


def set_instance_param(doc, category = BuiltInCategory.OST_Mass, inst_name = 'BoxFamily'):
    t = Transaction(doc, 'Modify existing family instances.')
     
    t.Start()
     
    collector = FilteredElementCollector(doc)
    collector.OfCategory(category)
    collector.OfClass(FamilyInstance)
     
    famtypeitr = collector.GetElementIdIterator()
    famtypeitr.Reset()
     
    inc = 1
     
    for famtypeID in famtypeitr:
        faminst = doc.get_Element(famtypeID)
     
        if faminst.Name == inst_name:
            param = faminst.get_Parameter('height')
            param.Set(2*inc)
            inc = inc + 1
     
    t.Commit()

def collector_category_class(doc):
    pass

def get_family():
    #Family Class - the overall Family
    #Family Symbol - the types within the Family
    #    - Use FamilyName instead of .Name
    #Family Instance - Actual instances of a type
    
#     In a FilteredElementCollector; 
#     OfClass restricts the collector to only, i.e., FamilyInstance elements
#     OfCategory restricts the collector to i.e. 'doors'
#     ToList converts the output of the collector into a list

    
    
    """Family Class - This object gets the family symbols that belong to the family so that instances can be swapped from one symbol to another. 
    Families within the Revit API represented by three objects - Family, FamilySymbol and FamilyInstance. 
    Each object plays a significant part in the structure of Families. 
    The Family object represents the entire family such as an 'I Beam'. 
    You can think of that object as representing the entire family file on disk. 
    The Family object contains a number of FamilySymbols. 
    The FamilySymbol object represents a specific set of family settings within that Family 
    and represents what is known in the Revit user interface as a Type, such as 'W14x32'. 
    The FamilyInstance object represents an actual instance of that Type (FamilySymbol) within the Autodesk Revit project. 
    For example the FamilyInstance would be a single instance of a W14x32 column within the project. 
    Therefore: Each FamilyInstance has one FamilySymbol, e.g. an instance of a W14x32. Each FamilySymbol belongs to one Family,
    e.g. the W14x32 symbol belongs to an 'I Beam' family. Each Family will contain one or more FamilySymbols, 
    e.g. the 'I Beam' family contains a W14x32 symbol, a W12x32 symbol etc.    """

#-Views and Sheets---
def get_view_templates(doc):
    logging.debug("get_view_dict")
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_dict = dict()
    
    for v in floorplans:
        if v.IsTemplate:
            view_dict[v.ViewName] = v
  
    logging.debug("Returned {} view templates in dict".format(len(view_dict)))
    
    return view_dict    

def apply_template(doc, view):
    pass
#     
#     View viewTemplate = (from v in new FilteredElementCollector(doc)
#         .OfClass(typeof(View))
#         .Cast<View>()
#         where v.IsTemplate == true && v.Name == "MyViewTemplate"
#         select v)
#         .First();
# 
#     using (Transaction t = new Transaction(doc,"Set View Template"))
#     {
#         t.Start();           
#         doc.ActiveView.ViewTemplateId = viewTemplate.Id;
#         t.Commit();
#     }
# }    



def get_all_views(doc):
    logging.debug("get_all_views")
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_dict = dict()
    
    for v in floorplans:
        if not v.IsTemplate:
            #print(v.ViewName,v.ViewType,v.IsTemplate)
            view_dict[v.ViewName] = v

    logging.debug("Returned {} views in dict (no view templates)".format(len(view_dict)))
    
    return view_dict

def get_views_by_type(doc, view_type):

    logging.debug("get_view_dict")
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_dict = dict()
    
    for v in floorplans:
        if not v.IsTemplate and v.ViewType.__str__() == view_type:
            view_dict[v.ViewName] = v

    logging.debug("Returned {} {} in dict (no view templates)".format(len(view_dict), view_type))
    
    return(view_dict)

# def get_all_title_blocks(doc):
#     logging.debug("get_sheet_types")
#     
#     
#     return collector 
#     
def get_title_blocks(doc):
    logging.debug("get_title_block")

    this_category = BuiltInCategory.OST_TitleBlocks
    this_class = FamilySymbol
    
    collector = FilteredElementCollector(doc)
    collector.OfCategory(this_category)
    collector.OfClass(this_class)
    
    #collector = get_all_title_blocks(doc)
    
    title_block_dict = dict()
    
    for elem in collector:
        title_block_dict[elem.FamilyName]=elem

    logging.debug("Returned {} title blocks".format(len(title_block_dict)))
    
    return(title_block_dict)

# def print_title_blocks(doc):
#     
#     collector = get_all_title_blocks(doc)
#     #collector.ToElements()
#     #elem_list = [el for el in collector]
#     #logging.debug("{} elements".format(len(elem_list)))
# 
#     print("{:30} | {:30} |".format("Name:","ID:"))
#     for elem in collector:
#         print("{:30} | {:30} ".format(elem.FamilyName,elem.Id))
#     
    #for item in dir(elem):
    #    print(item)
        #print(elem.Name)
        #print(dir(elem))
    #print(elems)
    
    #raise
#     print(dir(collector))
#     
#     print(len(collector))
#     
#     
#     
#     for elem in collector.GetElementIterator():
#         print(elem)
#         print(elem.Name)
    
    
    #print(collector.ToList())

def add_view_sheet(doc, sheet, view, center_pt):
    logging.debug("add_view_sheet")
    
    with Trans(doc, "Add view to sheet"):
        rvt_db.Viewport.Create(doc, sheet.Id, view.Id, center_pt)
    
    logging.debug("View {} placed on sheet {} {} at {}".format(view.Name, sheet.Name, sheet.SheetNumber, center_pt))

def get_element_from_id(doc, id_int):

    elem_id = rvt_db.ElementId(id_int)
    elem = doc.GetElement(elem_id)
    
    return elem

def get_uv_center(this_sheet):

    #print(this_sheet.Outline)
    #print()
    #print()
    
    center_u = (this_sheet.Outline.Max[0] - this_sheet.Outline.Min[0])/2 + this_sheet.Outline.Min[0]
    center_v = (this_sheet.Outline.Max[1] - this_sheet.Outline.Min[1])/2 + this_sheet.Outline.Min[1]
    centerUV = rvt_db.UV(center_u,center_v) 
    
    logging.debug("Box {} {} with center point {}".format(this_sheet.Outline.Min, this_sheet.Outline.Max, centerUV))
    return centerUV

    
def create_dependent(doc, active_view, part_name):
    # Copy current view as dependant\
    logging.debug("create_dependent".format())
    with Trans(doc, "Duplicate"):
        new_view_id = active_view.Duplicate(rvt_db.ViewDuplicateOption.AsDependent)
        new_view = doc.GetElement(new_view_id)
    
    new_name = new_view.Name.replace("Dependent 1", part_name)

    with Trans(doc, "Rename"):
        new_view.Name = new_name
    
    logging.debug("Created {}".format(new_view.Name))
    return new_view


def create_sheet(doc, title_block, name, number):
    logging.debug("create_sheet")
    
    title_block_id = title_block.Id
    with Trans(doc, "Create sheet"):
        new_sheet = rvt_db.ViewSheet.Create(doc, title_block_id)
        new_sheet.Name = name
        new_sheet.SheetNumber = number
        
    return new_sheet

    
    
    """
     Code Region: ViewSheet.Create()

    public static ViewSheet ViewSheet.Create(Document document, ElementId titleBlockTypeId);

    The newly created sheet has no floorplans. The Viewport.Create() method is used to add floorplans. 
    The Viewport class is used to add regular floorplans to a view sheet, i.e. plan, elevation, 
    drafting and three dimensional. To add schedules to a view, use ScheduleSheetInstance.Create() instead. 
    """
    
    #print(ViewSheet)
#     rvt_db.View#
#     
#     title_blocks = rvt_doc.TitleBlocks;
#     if (lend(title_blocks) == 0):
#         raise(Exception("No title blocks"))
#     
#     print(title_blocks)
    
    # Copy current view as dependant
    #t = Transaction(doc, 'This is my new transaction')
    #t.Start()
    #new_view_id = active_view.Duplicate(ViewDuplicateOption.AsDependent)
    #new_view = doc.GetElement(new_view_id)
    #t.Commit()
    
    #new_name = new_view.Name.replace("Dependent 1", part_name)
    
    #t.Start()
    #new_view.Name = new_name
    #t.Commit()

def get_sheet_dict(doc):
    logging.debug("get_sheet dict")
    cl_sheets = FilteredElementCollector(doc)
    
    sheets = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    
    sheet_dict = dict()
    for s in sheets:
        sheet_dict[s.Name] = s
        
    #logging.debug("Returned {} floorplans in dict".format(len(view_dict)))
    
    logging.debug("Returned {} sheets in dictionary".format(len(sheets)))
    
    return sheet_dict

def get_sheets(doc):
    logging.debug("get_sheets")
    cl_sheets = FilteredElementCollector(doc)
    
    sheetsnotsorted = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    sheets = sorted(sheetsnotsorted, key=lambda x: x.SheetNumber)
    
    logging.debug("Found {} sheets".format(len(sheets)))
    
    for s in sheets:
        print(s)
        #print(s.Parameter['Sheet Number'])
        #print(s.Parameter['Sheet Number'].AsString())
        #print('NUMBER: {0}   NAME:{1}'.format(    s.Parameter['Sheet Number'].AsString().rjust(10),
        #                s.Parameter['Sheet Name'].AsString().ljust(50),
        #    ))
        
    return(sheets)

#-Selection---
def selection(uidoc,doc):
    logging.debug(get_self())
    #print(uidoc.Selection)
    for el_ID in uidoc.Selection.GetElementIds():
        el = doc.GetElement(el_ID)
        logging.debug("Selected: {} {}".format(el_ID,el))        
    
def single_selection(uidoc,doc):
    logging.debug(get_self())
    selection = uidoc.Selection.GetElementIds()
    assert len(selection) == 1, "*Must select one and only one element*"
    for el_ID in selection:
        el = doc.GetElement(el_ID)
    logging.debug("Returning element: {} {}".format(el_ID,el))                
    return el

def parameter_exists(el, param_name):
    #if p in el.Parameters: return True
    #else: return False
    for p in el.Parameters:
        if p.Definition.Name == param_name:
            return True
    return False

def get_parameter_value(el, param_name):
    for p in el.Parameters:
        if p.Definition.Name == param_name:
            target_param = p
            #this_name = p.AsString()
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,p.AsString()))
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,this_name))
            break
            
    #return_str = p.AsString()
    #print("Returning {}")
    return p.AsString()
#        p.Definition.Name AsString 

def change_parameter(doc, el, param_name, new_value):
    logging.debug(get_self())
    
    target_param = None
    for p in el.Parameters:
        #print(p.Definition.Name)
        if p.Definition.Name == param_name:
            target_param = p
            break
    assert target_param, "{} not found".format(param_name)
    this_type = target_param.Definition.ParameterType
    target_type = rvt_db.ParameterType.Text
    assert this_type == target_type, "This function only works {}, not {}".format(target_type,this_type)
  
    with Trans(doc, "Change param"):
        target_param.Set(new_value)
        
    logging.debug("Overwrite {} from {} to {} in ".format(target_param.Definition.Name,
                                                    target_param.AsString(),
                                                    new_value,
                                                    target_param.Element))  
        
def table_parameters(el):

    logging.debug(get_self())

    print("{:20}".format("-name-").encode('utf-8'), end="")
    print("{:20}".format("-ParameterGroup-").encode('ascii'), end="")
    print("{:30}".format("-ParameterType-").encode('ascii'), end="")
    print("{:30}".format("-Value String-").encode('ascii'), end="")
    print("{:30}".format("-String-").encode('ascii'), end="")
    print("{:30}".format("-UnitType-").encode('ascii'), end="")
    print("")

    for param in el.Parameters:
        print("{0!s:20}".format(param.Definition.Name), end="")
        print("{0!s:20}".format(param.Definition.ParameterGroup), end="")
        print("{0!s:30}".format(param.Definition.ParameterType), end="")
        print("{0!s:30}".format(param.AsValueString()), end="")
        print("{0!s:30}".format(param.AsString()), end="")
        print("{0!s:30}".format(param.Definition.UnitType), end="")
        print("")
        
def list_parameters(el):
    logging.debug(get_self())
    for param in el.Parameters:
        print("Definition: {}".format(param.Definition))
        print("Definition.Name: {}".format(param.Definition.Name))        
        print("Definition.ParameterGroup: {}".format(param.Definition.ParameterGroup))        
        print("Definition.ParameterType: {}".format(param.Definition.ParameterType))        
        print("Definition.UnitType: {}".format(param.Definition.UnitType))
        
        print("param.AsString(): {}".format(param.AsString()))
        print("param.AsValueString(): {}".format(param.AsValueString()))
        print("param.AsElementId(): {}".format(param.AsElementId()))
        
        print("param: {}".format(param))
        #print("DisplayUnitType: {}".format(param.DisplayUnitType))
        print("Element: {}".format(param.Element))
        #print("GUID: {}".format(param.GUID))
        print("HasValue: {}".format(param.HasValue))
        print("Id: {}".format(param.Id))
        print("IsReadOnly: {}".format(param.IsReadOnly))
        print("IsShared: {}".format(param.IsShared))
        print("StorageType: {}".format(param.StorageType))
       
def inspect_selection(el):
    print("Name {}".format(el.Name))
    print("GetType {}".format(el.GetType()))
    print("GetTypeId {}".format(el.GetTypeId()))
    print("Parameter {}".format(el.Parameter))
    print("Parameters {}".format(el.Parameters))
    print("ParametersMap {}".format(el.ParametersMap))    
    
    print("GetOrderedParameters {}".format(el.GetOrderedParameters()))
    print("GetParameters {} -NEEDS PARAM NAME- ".format(el.GetParameters))

def project_parameters(doc):
    #import clr
    #from Autodesk.Revit.DB import InstanceBinding, TypeBinding, FilteredElementCollector, Transaction, ElementId

    pm = doc.ParameterBindings
    it = pm.ForwardIterator()
    it.Reset()
    
    deflist = []
    paramidlist = set()
    while(it.MoveNext()):
        p = it.Key
        b = pm[ p ]
    
        if isinstance(b, rvt_db.InstanceBinding):
            bind = 'Instance'
        elif isinstance(b, rvt_db.TypeBinding):
            bind = 'Type'
        else:
            bind = 'Unknown'
    
        print('\n')
        print('-'*100)
        print('PARAM: {0:<30} UNIT: {1:<10} TYPE: {2:<10} GROUP: {3:<20} BINDING: {4:<10} VISIBLE: {6}\nAPPLIED TO: {5}\n'.format(
                p.Name,
                str(p.UnitType),
                str(p.ParameterType),
                str(p.ParameterGroup),
                bind,
                [cat.Name for cat in b.Categories],
                p.Visible
                ))
        deflist.append( p )

def document_parameters(doc):
    logging.debug(get_self())
    params = FilteredElementCollector(doc).OfClass(rvt_db.ParameterElement)
#   filteredparams = []
    
    for param in params:
#        #Store parameters which has a name starting with "magi" or "MC"
#         if param.Name.startswith(("magi", "MC")): #startswith method accept tuple
#             filteredparams.append(param)            
        print(param.Name)
        


#-Properties---
def list_properties(doc,id):
    print()
    
#-Get objects---
def get_element_by_id(doc,id):
    return doc.GetElement(id)

def get_element_OST_Walls_ActiveView(doc):
    fec = rvt_db.FilteredElementCollector(doc, doc.ActiveView.Id)
    fec.OfCategory(BuiltInCategory.OST_Walls);
    
def get_element_OST_Walls_Document(doc):
    fec = rvt_db.FilteredElementCollector(doc)
    fec.OfCategory(BuiltInCategory.OST_Walls);

def apply_crop(doc,view, bound_box):
    logging.debug("apply_crop")
    
    # Adjust Crop on existing
    crop_manager = view.GetCropRegionShapeManager()
    logging.debug("Crop manager valid {}".format(crop_manager.Valid))
    
    #if 0 :
        #assert crop_manager.Valid, "Crop manager invalid"

    with Trans(doc, "Adjust crop"):
        crop_manager.SetCropRegionShape(bound_box)
        crop_manager.SetCropShape(bound_box)
        logging.debug("Cropped {}".format(view))



def get_grids(doc):
    logging.debug("get_grids")
    # Collect all grids in entire project to a name:element Dict
    collector = FilteredElementCollector(doc)
    collector.OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType()
    collect_grids = collector.ToElements()

    grid_dict = {}

    for grid in collect_grids:
        grid_name = grid.GetParameters('Name')[0].AsString()
        grid_dict[grid_name] = grid
    
    #for k,v in grid_dict.items():
        #    print(k,v)
    logging.debug("Returned {} grids".format(len(grid_dict)))
    return grid_dict

#-Geometry---
def get_bound_box(grid_bounds, oversize_factor):
    logging.debug("get_grids")
    
    # Given a dict of l,r,t,b to grid elements
    # Return a bonding box CurveLoop object
    # With rectangle increased oversize_factor
    
    # Get the X and Y unscaled bounds
    left_x = grid_bounds['left'].Curve.GetEndPoint(0).X
    right_x = grid_bounds['right'].Curve.GetEndPoint(0).X
    bot_y = grid_bounds['bot'].Curve.GetEndPoint(0).Y
    top_y = grid_bounds['top'].Curve.GetEndPoint(0).Y
    
    # Temporarily create box lines, to get scale factor
    top_line = Line.CreateBound(XYZ(left_x, top_y, 0), XYZ(right_x, top_y, 0))
    right_line = Line.CreateBound(XYZ(right_x, top_y, 0), XYZ(right_x, bot_y, 0))
    bot_line = Line.CreateBound(XYZ(right_x, bot_y, 0), XYZ(left_x, bot_y, 0))
    left_line = Line.CreateBound(XYZ(left_x, bot_y, 0), XYZ(left_x, top_y, 0))
    
    # Calculate scale adjustments
    X_scale = top_line.Length*oversize_factor
    Y_scale = right_line.Length*oversize_factor
    
    # Apply the scaling
    left_x = grid_bounds['left'].Curve.GetEndPoint(0).X - X_scale
    right_x = grid_bounds['right'].Curve.GetEndPoint(0).X + X_scale
    bot_y = grid_bounds['bot'].Curve.GetEndPoint(0).Y - Y_scale
    top_y = grid_bounds['top'].Curve.GetEndPoint(0).Y + Y_scale

    # Create the scaled box lines
    top_line = Line.CreateBound(XYZ(left_x, top_y, 0), XYZ(right_x, top_y, 0))
    right_line = Line.CreateBound(XYZ(right_x, top_y, 0), XYZ(right_x, bot_y, 0))
    bot_line = Line.CreateBound(XYZ(right_x, bot_y, 0), XYZ(left_x, bot_y, 0))
    left_line = Line.CreateBound(XYZ(left_x, bot_y, 0), XYZ(left_x, top_y, 0))
        
    # Create a loop object
    bound_box = CurveLoop()    
    # Need to APPEND the lines
    bound_box.Append(top_line)
    bound_box.Append(right_line)
    bound_box.Append(bot_line)
    bound_box.Append(left_line)    
    
    assert not bound_box.IsOpen(), "Box not closed"
    
    print("Created curve element box".format(grid_bounds))

    return bound_box


