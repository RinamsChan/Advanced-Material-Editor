bl_info = {
    "name": "Advanced Material Editor",
    "author": "407ro4d",
    "version": (2, 2, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Tools",
    "description": "Расширенный редактор материалов с порошковым покрытием, блестками, градиентами и пресетами",
    "category": "Material",
}

import bpy
import mathutils
from bpy.types import Panel, Operator, PropertyGroup, AddonPreferences
from bpy.props import (FloatProperty, PointerProperty, BoolProperty, 
                      FloatVectorProperty, IntProperty, EnumProperty)

# Словарь с переводами
translations_dict = {
    "ru_RU": {
        ("*", "Advanced Material Editor"): "Расширенный редактор материалов",
        ("*", "Main Settings"): "Основные настройки",
        ("*", "Basic BSDF Parameters"): "Базовые параметры BSDF",
        ("*", "Powder Coating"): "Порошковое покрытие",
        ("*", "Metallic Sparkles"): "Металлические блестки",
        ("*", "Gradient Materials"): "Градиентные материалы",
        ("*", "Alpha Channel Tools"): "Инструменты Alpha канала",
        ("*", "Selected objects: %d"): "Выбрано объектов: %d",
        ("*", "Select mesh objects"): "Выберите меш-объекты",
        ("*", "Quick Editors:"): "Быстрые редакторы:",
        ("*", "Powder"): "Порошковое",
        ("*", "Sparkles"): "Блестки",
        ("*", "Gradient"): "Градиент",
        ("*", "Basic"): "Базовый",
        ("*", "Main parameters:"): "Основные параметры:",
        ("*", "Update Materials"): "Применить изменения",
        ("*", "Reset"): "Сбросить",
        ("*", "Copy from Active"): "Взять из активного",
        ("*", "Quick Presets:"): "Быстрые пресеты:",
        ("*", "Metal"): "Металл",
        ("*", "Plastic"): "Пластик",
        ("*", "Glass"): "Стекло",
        ("*", "Rubber"): "Резина",
        ("*", "Ceramic"): "Керамика",
        ("*", "Wood"): "Дерево",
        ("*", "Powder Coating Settings:"): "Настройки покрытия:",
        ("*", "Base Roughness"): "Шероховатость основы",
        ("*", "Clearcoat"): "Защитный слой",
        ("*", "Flakes:"): "Блестки:",
        ("*", "Flake Density"): "Плотность блесток",
        ("*", "Flake Size"): "Размер блесток",
        ("*", "Flake Metallic"): "Металличность блесток",
        ("*", "Flake Roughness"): "Шероховатость блесток",
        ("*", "Create Powder Coating"): "Создать порошковое покрытие",
        ("*", "Main Sparkle Settings:"): "Основные настройки блесток:",
        ("*", "Intensity"): "Интенсивность",
        ("*", "Threshold"): "Порог",
        ("*", "Sparkle Texture:"): "Текстура блесток:",
        ("*", "Scale"): "Масштаб",
        ("*", "Detail"): "Детализация",
        ("*", "Roughness"): "Шероховатость",
        ("*", "Sparkle Color:"): "Цвет блесток:",
        ("*", "Create Sparkle Material"): "Создать материал с блестками",
        ("*", "Gradient Type:"): "Тип градиента:",
        ("*", "Gradient Colors:"): "Цвета градиента:",
        ("*", "Use Three Colors"): "Три цвета",
        ("*", "Color 1"): "Цвет 1",
        ("*", "Color 2"): "Цвет 2",
        ("*", "Color 3"): "Цвет 3",
        ("*", "Transformation:"): "Трансформация:",
        ("*", "Rotation"): "Поворот",
        ("*", "Scale"): "Масштаб",
        ("*", "Offset"): "Смещение",
        ("*", "Create Gradient Material"): "Создать градиентный материал",
        ("*", "Connect Alpha to BSDF:"): "Подключить Alpha к BSDF:",
        ("*", "For Selected Objects"): "Для выбранных объектов",
        ("*", "For All Materials"): "Для всех материалов сцены",
        ("*", "Metallic"): "Металличность",
        ("*", "Specular/IOR"): "Отражение/IOR",
        ("*", "Clearcoat Roughness"): "Шероховатость покрытия",
        ("*", "Language"): "Язык",
        ("*", "Select interface language"): "Выберите язык интерфейса",
        ("*", "Russian"): "Русский",
        ("*", "English"): "Английский",
        ("*", "Materials updated: %d"): "Обновлено материалов: %d",
        ("*", "Values reset"): "Значения сброшены",
        ("*", "Active object has no materials"): "Активный объект не имеет материалов",
        ("*", "Values copied from active object"): "Значения скопированы из активного объекта",
        ("*", "Principled BSDF not found in active object"): "Не найден Principled BSDF в материалах активного объекта",
        ("*", "Preset applied:"): "Применен пресет:",
        ("*", "Created powder coating for %d objects"): "Созданы материалы с порошковым покрытием для %d объектов",
        ("*", "Created sparkle materials for %d objects"): "Созданы материалы с блестками для %d объектов",
        ("*", "Created gradient materials for %d objects"): "Созданы градиентные материалы для %d объектов",
        ("*", "Alpha channels connected: %d in %d materials"): "Подключено альфа-каналов: %d в %d материалах",
        ("*", "No suitable materials found for alpha connection"): "Не найдено подходящих материалов для подключения альфа-каналов",
        ("*", "Processed materials: %d, connections: %d"): "Обработано материалов: %d, подключений: %d",
    }
}

# Глобальная переменная для хранения текущего языка
current_language = 'ru_RU'

# Функция для перевода
def tr(text):
    """Перевод текста на текущий язык интерфейса"""
    global current_language
    # Принудительно устанавливаем локаль для переводов
    if current_language in translations_dict:
        translations = translations_dict[current_language]
        if ("*", text) in translations:
            return translations[("*", text)]
    return text

# Класс настроек аддона
class AdvancedMaterialEditorPreferences(AddonPreferences):
    bl_idname = __name__
    
    language: EnumProperty(
        name="Language",
        description="Select interface language",
        items=[
            ('ru_RU', "Русский", "Russian"),
            ('en_US', "English", "English"),
        ],
        default='ru_RU',
        update=lambda self, context: update_language(self, context)
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "language")

def update_language(self, context):
    """Обновляет язык при изменении настройки"""
    global current_language
    current_language = self.language
    # Принудительно обновляем все области
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()

class PrincipledProperties(PropertyGroup):
    # Основные параметры
    metallic: FloatProperty(
        name="Metallic",
        description="Metallic значение",
        min=0.0,
        max=1.0,
        default=0.0,
        subtype='FACTOR'
    )
    
    roughness: FloatProperty(
        name="Roughness",
        description="Roughness значение",
        min=0.0,
        max=1.0,
        default=0.5,
        subtype='FACTOR'
    )
    
    specular: FloatProperty(
        name="Specular/IOR",
        description="Specular или IOR значение в зависимости от версии Blender",
        min=0.0,
        max=2.0,
        default=0.5,
        subtype='FACTOR'
    )
    
    clearcoat: FloatProperty(
        name="Clearcoat",
        description="Clearcoat значение",
        min=0.0,
        max=1.0,
        default=0.0,
        subtype='FACTOR'
    )
    
    clearcoat_roughness: FloatProperty(
        name="Clearcoat Roughness",
        description="Clearcoat Roughness значение",
        min=0.0,
        max=1.0,
        default=0.0,
        subtype='FACTOR'
    )

class PowderCoatingProperties(PropertyGroup):
    # Параметры порошкового покрытия
    base_roughness: FloatProperty(
        name="Base Roughness",
        description="Base material roughness",
        min=0.0,
        max=1.0,
        default=0.3,
        subtype='FACTOR'
    )
    
    flake_density: FloatProperty(
        name="Flake Density",
        description="Number of flakes on surface",
        min=0.0,
        max=1.0,
        default=0.5,
        subtype='FACTOR'
    )
    
    flake_size: FloatProperty(
        name="Flake Size",
        description="Size of individual flakes",
        min=0.01,
        max=0.5,
        default=0.1,
        subtype='FACTOR'
    )
    
    flake_metallic: FloatProperty(
        name="Flake Metallic",
        description="Metallic effect of flakes",
        min=0.0,
        max=1.0,
        default=0.8,
        subtype='FACTOR'
    )
    
    flake_roughness: FloatProperty(
        name="Flake Roughness",
        description="Roughness of flake surface",
        min=0.0,
        max=1.0,
        default=0.2,
        subtype='FACTOR'
    )
    
    clearcoat: FloatProperty(
        name="Clearcoat",
        description="Clearcoat thickness",
        min=0.0,
        max=1.0,
        default=0.7,
        subtype='FACTOR'
    )

class SparklesProperties(PropertyGroup):
    # Параметры блесток
    sparkle_intensity: FloatProperty(
        name="Intensity",
        description="Brightness and visibility of sparkles",
        min=0.0,
        max=2.0,
        default=1.0,
        subtype='FACTOR'
    )
    
    sparkle_scale: FloatProperty(
        name="Scale",
        description="Sparkle pattern scale",
        min=1.0,
        max=100.0,
        default=50.0
    )
    
    sparkle_detail: FloatProperty(
        name="Detail",
        description="Sparkle pattern detail",
        min=0.0,
        max=16.0,
        default=8.0
    )
    
    sparkle_roughness: FloatProperty(
        name="Roughness",
        description="Sparkle pattern roughness",
        min=0.0,
        max=1.0,
        default=0.3,
        subtype='FACTOR'
    )
    
    sparkle_color: FloatVectorProperty(
        name="Sparkle Color",
        description="Color of metallic sparkles",
        subtype='COLOR',
        size=3,
        default=(1.0, 0.9, 0.5),
        min=0.0,
        max=1.0
    )
    
    threshold: FloatProperty(
        name="Threshold",
        description="Threshold for creating individual sparkles",
        min=0.0,
        max=1.0,
        default=0.7,
        subtype='FACTOR'
    )

class GradientProperties(PropertyGroup):
    # Параметры градиента
    gradient_type: EnumProperty(
        name="Gradient Type",
        description="Gradient texture type",
        items=[
            ('LINEAR', "Linear", "Linear gradient"),
            ('RADIAL', "Radial", "Radial gradient"),
            ('QUADRATIC', "Quadratic", "Quadratic gradient"),
            ('SPHERICAL', "Spherical", "Spherical gradient")
        ],
        default='LINEAR'
    )
    
    gradient_color1: FloatVectorProperty(
        name="Color 1",
        description="First gradient color",
        subtype='COLOR',
        size=3,
        default=(0.1, 0.3, 0.8),
        min=0.0,
        max=1.0
    )
    
    gradient_color2: FloatVectorProperty(
        name="Color 2",
        description="Second gradient color",
        subtype='COLOR',
        size=3,
        default=(0.8, 0.2, 0.1),
        min=0.0,
        max=1.0
    )
    
    gradient_color3: FloatVectorProperty(
        name="Color 3",
        description="Third gradient color (optional)",
        subtype='COLOR',
        size=3,
        default=(0.9, 0.9, 0.1),
        min=0.0,
        max=1.0
    )
    
    use_three_colors: BoolProperty(
        name="Use Three Colors",
        description="Use three colors instead of two",
        default=False
    )
    
    gradient_rotation: FloatProperty(
        name="Rotation",
        description="Gradient rotation",
        min=0.0,
        max=6.28319,
        default=0.0,
        subtype='ANGLE'
    )
    
    gradient_scale: FloatProperty(
        name="Scale",
        description="Gradient scale",
        min=0.1,
        max=10.0,
        default=1.0
    )
    
    gradient_offset: FloatVectorProperty(
        name="Offset",
        description="Gradient offset",
        subtype='TRANSLATION',
        size=3,
        default=(0.0, 0.0, 0.0)
    )

# Общие функции
def connect_alpha_to_bsdf(material):
    """Подключает альфа-канал всех Image Texture к Principled BSDF в материале"""
    if not material.use_nodes:
        return False
    
    node_tree = material.node_tree
    principled_bsdf = None
    image_textures = []
    
    for node in node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_bsdf = node
        elif node.type == 'TEX_IMAGE':
            image_textures.append(node)
    
    if not principled_bsdf or not image_textures:
        return False
    
    connected_count = 0
    for tex_node in image_textures:
        if tex_node.outputs['Alpha'].is_linked:
            continue
        node_tree.links.new(tex_node.outputs['Alpha'], principled_bsdf.inputs['Alpha'])
        connected_count += 1
    
    return connected_count > 0

def safe_set_input(principled_node, input_name, value):
    """Безопасно устанавливает значение входа, если он существует"""
    try:
        principled_node.inputs[input_name].default_value = value
        return True
    except KeyError:
        return False

def safe_get_input(principled_node, input_name, default_value=None):
    """Безопасно получает значение входа, если он существует"""
    try:
        return principled_node.inputs[input_name].default_value
    except KeyError:
        return default_value

# Операторы для Principled BSDF
class PRINCIPLED_OT_update_materials(Operator):
    """Обновить материалы выбранных объектов"""
    bl_idname = "principled.update_materials"
    bl_label = "Update Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, tr("Select mesh objects"))
            return {'CANCELLED'}
        
        updated_count = 0
        
        for obj in selected_objects:
            if obj.material_slots:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        nodes = mat_slot.material.node_tree.nodes
                        principled_node = None
                        for node in nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                principled_node = node
                                break
                        
                        if principled_node:
                            safe_set_input(principled_node, 'Metallic', principled_tool.metallic)
                            safe_set_input(principled_node, 'Roughness', principled_tool.roughness)
                            safe_set_input(principled_node, 'Specular', principled_tool.specular)
                            safe_set_input(principled_node, 'IOR', principled_tool.specular)
                            safe_set_input(principled_node, 'Clearcoat', principled_tool.clearcoat)
                            safe_set_input(principled_node, 'Clearcoat Roughness', principled_tool.clearcoat_roughness)
                            updated_count += 1
        
        self.report({'INFO'}, tr("Materials updated: %d") % updated_count)
        return {'FINISHED'}

class PRINCIPLED_OT_reset_values(Operator):
    """Сбросить значения к стандартным"""
    bl_idname = "principled.reset_values"
    bl_label = "Reset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.5
        principled_tool.specular = 0.5
        principled_tool.clearcoat = 0.0
        principled_tool.clearcoat_roughness = 0.0
        
        self.report({'INFO'}, tr("Values reset"))
        return {'FINISHED'}

class PRINCIPLED_OT_copy_from_active(Operator):
    """Скопировать значения из активного объекта"""
    bl_idname = "principled.copy_from_active"
    bl_label = "Copy from Active"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_obj = context.active_object
        
        if not active_obj or active_obj.type != 'MESH' or not active_obj.material_slots:
            self.report({'WARNING'}, tr("Active object has no materials"))
            return {'CANCELLED'}
        
        scene = context.scene
        principled_tool = scene.principled_tool
        
        for mat_slot in active_obj.material_slots:
            if mat_slot.material and mat_slot.material.use_nodes:
                nodes = mat_slot.material.node_tree.nodes
                for node in nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        principled_tool.metallic = safe_get_input(node, 'Metallic', 0.0)
                        principled_tool.roughness = safe_get_input(node, 'Roughness', 0.5)
                        
                        specular_val = safe_get_input(node, 'Specular', None)
                        if specular_val is not None:
                            principled_tool.specular = specular_val
                        else:
                            principled_tool.specular = safe_get_input(node, 'IOR', 0.5)
                        
                        principled_tool.clearcoat = safe_get_input(node, 'Clearcoat', 0.0)
                        principled_tool.clearcoat_roughness = safe_get_input(node, 'Clearcoat Roughness', 0.0)
                        
                        self.report({'INFO'}, tr("Values copied from active object"))
                        return {'FINISHED'}
        
        self.report({'WARNING'}, tr("Principled BSDF not found in active object"))
        return {'CANCELLED'}

# Пресеты материалов
class PRINCIPLED_OT_preset_metal(Operator):
    """Установить пресет металла"""
    bl_idname = "principled.preset_metal"
    bl_label = "Metal"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 1.0
        principled_tool.roughness = 0.2
        principled_tool.specular = 0.5
        principled_tool.clearcoat = 0.0
        principled_tool.clearcoat_roughness = 0.1
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Metal")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_plastic(Operator):
    """Установить пресет пластика"""
    bl_idname = "principled.preset_plastic"
    bl_label = "Plastic"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.4
        principled_tool.specular = 0.5
        principled_tool.clearcoat = 0.0
        principled_tool.clearcoat_roughness = 0.0
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Plastic")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_glass(Operator):
    """Установить пресет стекла"""
    bl_idname = "principled.preset_glass"
    bl_label = "Glass"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.0
        principled_tool.specular = 1.45
        principled_tool.clearcoat = 0.0
        principled_tool.clearcoat_roughness = 0.0
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Glass")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_rubber(Operator):
    """Установить пресет резины"""
    bl_idname = "principled.preset_rubber"
    bl_label = "Rubber"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.8
        principled_tool.specular = 0.5
        principled_tool.clearcoat = 0.0
        principled_tool.clearcoat_roughness = 0.0
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Rubber")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_ceramic(Operator):
    """Установить пресет керамики"""
    bl_idname = "principled.preset_ceramic"
    bl_label = "Ceramic"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.1
        principled_tool.specular = 0.9
        principled_tool.clearcoat = 0.3
        principled_tool.clearcoat_roughness = 0.1
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Ceramic")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_wood(Operator):
    """Установить пресет дерева"""
    bl_idname = "principled.preset_wood"
    bl_label = "Wood"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.0
        principled_tool.roughness = 0.7
        principled_tool.specular = 0.3
        principled_tool.clearcoat = 0.2
        principled_tool.clearcoat_roughness = 0.3
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Wood")
        return {'FINISHED'}

class PRINCIPLED_OT_preset_powder_coating(Operator):
    """Установить пресет порошкового покрытия с блестками"""
    bl_idname = "principled.preset_powder_coating"
    bl_label = "Powder Coating"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        principled_tool = scene.principled_tool
        
        principled_tool.metallic = 0.1
        principled_tool.roughness = 0.3
        principled_tool.specular = 0.8
        principled_tool.clearcoat = 0.7
        principled_tool.clearcoat_roughness = 0.2
        
        bpy.ops.principled.update_materials()
        self.report({'INFO'}, tr("Preset applied:") + " Powder Coating")
        return {'FINISHED'}

# Операторы для порошкового покрытия
class POWDER_OT_create_coating(Operator):
    """Создать материал с порошковым покрытием"""
    bl_idname = "powder.create_coating"
    bl_label = "Create Powder Coating"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        powder_tool = scene.powder_coating_tool
        
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, tr("Select mesh objects"))
            return {'CANCELLED'}
        
        for obj in selected_objects:
            mat_name = f"Powder_Coating_{obj.name}"
            material = bpy.data.materials.new(name=mat_name)
            material.use_nodes = True
            
            nodes = material.node_tree.nodes
            links = material.node_tree.links
            nodes.clear()
            
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled.location = (0, 0)
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (400, 0)
            
            noise = nodes.new(type='ShaderNodeTexNoise')
            noise.location = (-600, 200)
            noise.inputs['Scale'].default_value = powder_tool.flake_density * 100 + 10
            noise.inputs['Detail'].default_value = 8.0
            noise.inputs['Roughness'].default_value = powder_tool.flake_roughness
            
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.location = (-400, 200)
            color_ramp.color_ramp.elements[0].position = 0.6
            color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
            color_ramp.color_ramp.elements[1].position = 0.8
            color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
            
            mix_shader = nodes.new(type='ShaderNodeMixShader')
            mix_shader.location = (200, 0)
            
            flake_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            flake_bsdf.location = (0, 200)
            flake_bsdf.inputs['Metallic'].default_value = powder_tool.flake_metallic
            flake_bsdf.inputs['Roughness'].default_value = powder_tool.flake_roughness
            flake_bsdf.inputs['Base Color'].default_value = (1.0, 0.9, 0.5, 1.0)
            
            principled.inputs['Roughness'].default_value = powder_tool.base_roughness
            principled.inputs['Metallic'].default_value = 0.0
            safe_set_input(principled, 'Clearcoat', powder_tool.clearcoat)
            
            tex_coord = nodes.new(type='ShaderNodeTexCoord')
            tex_coord.location = (-1000, 200)
            mapping = nodes.new(type='ShaderNodeMapping')
            mapping.location = (-800, 200)
            
            links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
            links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
            links.new(color_ramp.outputs['Color'], mix_shader.inputs['Fac'])
            links.new(principled.outputs['BSDF'], mix_shader.inputs[1])
            links.new(flake_bsdf.outputs['BSDF'], mix_shader.inputs[2])
            links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
            
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        
        self.report({'INFO'}, tr("Created powder coating for %d objects") % len(selected_objects))
        return {'FINISHED'}

# Операторы для блесток
class SPARKLES_OT_create_sparkles(Operator):
    """Создать продвинутый материал с блестками"""
    bl_idname = "sparkles.create_sparkles"
    bl_label = "Create Sparkle Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        sparkles_tool = scene.sparkles_tool
        
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, tr("Select mesh objects"))
            return {'CANCELLED'}
        
        for obj in selected_objects:
            mat_name = f"Sparkles_Material_{obj.name}"
            material = bpy.data.materials.new(name=mat_name)
            material.use_nodes = True
            
            nodes = material.node_tree.nodes
            links = material.node_tree.links
            nodes.clear()
            
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled.location = (0, 0)
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (400, 0)
            
            noise1 = nodes.new(type='ShaderNodeTexNoise')
            noise1.location = (-800, 300)
            noise1.inputs['Scale'].default_value = sparkles_tool.sparkle_scale
            noise1.inputs['Detail'].default_value = sparkles_tool.sparkle_detail
            noise1.inputs['Roughness'].default_value = sparkles_tool.sparkle_roughness
            
            noise2 = nodes.new(type='ShaderNodeTexNoise')
            noise2.location = (-800, 0)
            noise2.inputs['Scale'].default_value = sparkles_tool.sparkle_scale * 2
            noise2.inputs['Detail'].default_value = sparkles_tool.sparkle_detail
            
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.location = (-400, 200)
            color_ramp.color_ramp.elements[0].position = sparkles_tool.threshold - 0.2
            color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
            color_ramp.color_ramp.elements[1].position = sparkles_tool.threshold
            color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
            
            multiply = nodes.new(type='ShaderNodeMath')
            multiply.location = (-600, -200)
            multiply.operation = 'MULTIPLY'
            multiply.inputs[1].default_value = sparkles_tool.sparkle_intensity
            
            tex_coord = nodes.new(type='ShaderNodeTexCoord')
            tex_coord.location = (-1200, 200)
            mapping = nodes.new(type='ShaderNodeMapping')
            mapping.location = (-1000, 200)
            
            links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], noise1.inputs['Vector'])
            links.new(mapping.outputs['Vector'], noise2.inputs['Vector'])
            links.new(noise1.outputs['Fac'], multiply.inputs[0])
            links.new(noise2.outputs['Fac'], multiply.inputs[1])
            links.new(multiply.outputs['Value'], color_ramp.inputs['Fac'])
            
            try:
                links.new(color_ramp.outputs['Color'], principled.inputs['Specular'])
            except KeyError:
                try:
                    links.new(color_ramp.outputs['Color'], principled.inputs['IOR'])
                except KeyError:
                    pass
            
            emission = nodes.new(type='ShaderNodeEmission')
            emission.location = (0, 200)
            emission.inputs['Color'].default_value = (*sparkles_tool.sparkle_color, 1.0)
            emission.inputs['Strength'].default_value = sparkles_tool.sparkle_intensity
            
            mix_shader = nodes.new(type='ShaderNodeMixShader')
            mix_shader.location = (200, 0)
            links.new(color_ramp.outputs['Color'], mix_shader.inputs['Fac'])
            links.new(emission.outputs['Emission'], mix_shader.inputs[1])
            links.new(principled.outputs['BSDF'], mix_shader.inputs[2])
            links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
            
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        
        self.report({'INFO'}, tr("Created sparkle materials for %d objects") % len(selected_objects))
        return {'FINISHED'}

# Операторы для градиента
class GRADIENT_OT_create_gradient(Operator):
    """Создать материал с градиентом"""
    bl_idname = "gradient.create_gradient"
    bl_label = "Create Gradient Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        gradient_tool = scene.gradient_tool
        
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, tr("Select mesh objects"))
            return {'CANCELLED'}
        
        for obj in selected_objects:
            mat_name = f"Gradient_Material_{obj.name}"
            material = bpy.data.materials.new(name=mat_name)
            material.use_nodes = True
            
            nodes = material.node_tree.nodes
            links = material.node_tree.links
            nodes.clear()
            
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            principled.location = (0, 0)
            output = nodes.new(type='ShaderNodeOutputMaterial')
            output.location = (400, 0)
            
            if gradient_tool.gradient_type == 'LINEAR':
                gradient = nodes.new(type='ShaderNodeTexGradient')
                gradient.gradient_type = 'LINEAR'
            elif gradient_tool.gradient_type == 'RADIAL':
                gradient = nodes.new(type='ShaderNodeTexGradient')
                gradient.gradient_type = 'RADIAL'
            elif gradient_tool.gradient_type == 'QUADRATIC':
                gradient = nodes.new(type='ShaderNodeTexGradient')
                gradient.gradient_type = 'QUADRATIC'
            else:
                gradient = nodes.new(type='ShaderNodeTexGradient')
                gradient.gradient_type = 'SPHERICAL'
            
            gradient.location = (-600, 0)
            
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.location = (-400, 0)
            
            if gradient_tool.use_three_colors:
                color_ramp.color_ramp.elements[0].color = (*gradient_tool.gradient_color1, 1.0)
                color_ramp.color_ramp.elements[0].position = 0.0
                
                if len(color_ramp.color_ramp.elements) < 3:
                    color_ramp.color_ramp.elements.new(0.5)
                color_ramp.color_ramp.elements[1].color = (*gradient_tool.gradient_color2, 1.0)
                color_ramp.color_ramp.elements[1].position = 0.5
                
                color_ramp.color_ramp.elements[2].color = (*gradient_tool.gradient_color3, 1.0)
                color_ramp.color_ramp.elements[2].position = 1.0
            else:
                color_ramp.color_ramp.elements[0].color = (*gradient_tool.gradient_color1, 1.0)
                color_ramp.color_ramp.elements[0].position = 0.0
                color_ramp.color_ramp.elements[1].color = (*gradient_tool.gradient_color2, 1.0)
                color_ramp.color_ramp.elements[1].position = 1.0
                
                while len(color_ramp.color_ramp.elements) > 2:
                    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[1])
            
            mapping = nodes.new(type='ShaderNodeMapping')
            mapping.location = (-1000, 0)
            mapping.inputs['Rotation'].default_value = (0, 0, gradient_tool.gradient_rotation)
            mapping.inputs['Scale'].default_value = (gradient_tool.gradient_scale, gradient_tool.gradient_scale, gradient_tool.gradient_scale)
            mapping.inputs['Location'].default_value = gradient_tool.gradient_offset
            
            tex_coord = nodes.new(type='ShaderNodeTexCoord')
            tex_coord.location = (-1200, 0)
            
            links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
            links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])
            links.new(gradient.outputs['Color'], color_ramp.inputs['Fac'])
            links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
            links.new(principled.outputs['BSDF'], output.inputs['Surface'])
            
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
        
        self.report({'INFO'}, tr("Created gradient materials for %d objects") % len(selected_objects))
        return {'FINISHED'}

# Операторы для Alpha каналов
class PRINCIPLED_OT_connect_alpha_selected(Operator):
    """Подключить альфа-каналы у выбранных объектов"""
    bl_idname = "principled.connect_alpha_selected"
    bl_label = "Connect Alpha to Selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, tr("Select mesh objects"))
            return {'CANCELLED'}
        
        connected_materials = 0
        total_connections = 0
        
        for obj in selected_objects:
            if obj.material_slots:
                for mat_slot in obj.material_slots:
                    if mat_slot.material:
                        if connect_alpha_to_bsdf(mat_slot.material):
                            connected_materials += 1
                            node_tree = mat_slot.material.node_tree
                            if node_tree:
                                for node in node_tree.nodes:
                                    if node.type == 'TEX_IMAGE' and node.outputs['Alpha'].is_linked:
                                        total_connections += 1
        
        if connected_materials > 0:
            self.report({'INFO'}, tr("Alpha channels connected: %d in %d materials") % (total_connections, connected_materials))
        else:
            self.report({'WARNING'}, tr("No suitable materials found for alpha connection"))
        
        return {'FINISHED'}

class PRINCIPLED_OT_connect_alpha_all(Operator):
    """Подключить альфа-каналы во всех материалах сцены"""
    bl_idname = "principled.connect_alpha_all"
    bl_label = "Connect Alpha to All"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        connected_materials = 0
        total_connections = 0
        
        for material in bpy.data.materials:
            if connect_alpha_to_bsdf(material):
                connected_materials += 1
                node_tree = material.node_tree
                if node_tree:
                    for node in node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.outputs['Alpha'].is_linked:
                            total_connections += 1
        
        self.report({'INFO'}, tr("Processed materials: %d, connections: %d") % (connected_materials, total_connections))
        return {'FINISHED'}

# Панели
class VIEW3D_PT_material_editor_main(Panel):
    """Главная панель редактора материалов"""
    bl_label = "Advanced Material Editor"
    bl_idname = "VIEW3D_PT_material_editor_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        selected_count = len([obj for obj in context.selected_objects if obj.type == 'MESH'])
        layout.label(text=tr("Selected objects: %d") % selected_count)
        
        if selected_count == 0:
            layout.label(text=tr("Select mesh objects"), icon='ERROR')
            return
        
        layout.label(text=tr("Quick Editors:"), icon='MATERIAL')
        
        row = layout.row(align=True)
        row.operator("powder.create_coating", text=tr("Powder"), icon='PARTICLES')
        row.operator("sparkles.create_sparkles", text=tr("Sparkles"), icon='SHADING_RENDERED')
        
        row = layout.row(align=True)
        row.operator("gradient.create_gradient", text=tr("Gradient"), icon='COLOR')
        row.operator("principled.update_materials", text=tr("Basic"), icon='NODE_MATERIAL')

class VIEW3D_PT_basic_editor(Panel):
    """Базовый редактор Principled BSDF"""
    bl_label = "Basic BSDF Parameters"
    bl_idname = "VIEW3D_PT_basic_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "VIEW3D_PT_material_editor_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        principled_tool = scene.principled_tool
        
        layout.label(text=tr("Main parameters:"), icon='NODE_MATERIAL')
        
        layout.prop(principled_tool, "metallic", text=tr("Metallic"))
        layout.prop(principled_tool, "roughness", text=tr("Roughness"))
        layout.prop(principled_tool, "specular", text=tr("Specular/IOR"))
        layout.prop(principled_tool, "clearcoat", text=tr("Clearcoat"))
        layout.prop(principled_tool, "clearcoat_roughness", text=tr("Clearcoat Roughness"))
        
        layout.separator()
        
        row = layout.row()
        row.operator("principled.update_materials", icon='MATERIAL')
        row.operator("principled.reset_values", icon='LOOP_BACK')
        
        layout.operator("principled.copy_from_active", icon='COPY_ID')
        
        # Пресеты материалов
        layout.separator()
        layout.label(text=tr("Quick Presets:"), icon='PRESET')
        
        row = layout.row(align=True)
        row.operator("principled.preset_metal", text=tr("Metal"))
        row.operator("principled.preset_plastic", text=tr("Plastic"))
        
        row = layout.row(align=True)
        row.operator("principled.preset_glass", text=tr("Glass"))
        row.operator("principled.preset_rubber", text=tr("Rubber"))
        
        row = layout.row(align=True)
        row.operator("principled.preset_ceramic", text=tr("Ceramic"))
        row.operator("principled.preset_wood", text=tr("Wood"))
        
        row = layout.row(align=True)
        row.operator("principled.preset_powder_coating", text=tr("Powder"), icon='PARTICLES')

class VIEW3D_PT_powder_coating_editor(Panel):
    """Редактор порошкового покрытия"""
    bl_label = "Powder Coating"
    bl_idname = "VIEW3D_PT_powder_coating_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "VIEW3D_PT_material_editor_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        powder_tool = scene.powder_coating_tool
        
        layout.label(text=tr("Powder Coating Settings:"), icon='PARTICLES')
        
        layout.prop(powder_tool, "base_roughness", text=tr("Base Roughness"))
        layout.prop(powder_tool, "clearcoat", text=tr("Clearcoat"))
        
        layout.separator()
        layout.label(text=tr("Flakes:"), icon='RENDERLAYERS')
        
        layout.prop(powder_tool, "flake_density", text=tr("Flake Density"))
        layout.prop(powder_tool, "flake_size", text=tr("Flake Size"))
        layout.prop(powder_tool, "flake_metallic", text=tr("Flake Metallic"))
        layout.prop(powder_tool, "flake_roughness", text=tr("Flake Roughness"))
        
        layout.separator()
        layout.operator("powder.create_coating", icon='ADD', text=tr("Create Powder Coating"))

class VIEW3D_PT_sparkles_editor(Panel):
    """Редактор блесток"""
    bl_label = "Metallic Sparkles"
    bl_idname = "VIEW3D_PT_sparkles_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "VIEW3D_PT_material_editor_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        sparkles_tool = scene.sparkles_tool
        
        layout.label(text=tr("Main Sparkle Settings:"), icon='RENDERLAYERS')
        
        layout.prop(sparkles_tool, "sparkle_intensity", text=tr("Intensity"))
        layout.prop(sparkles_tool, "threshold", text=tr("Threshold"))
        
        layout.separator()
        layout.label(text=tr("Sparkle Texture:"), icon='TEXTURE')
        
        layout.prop(sparkles_tool, "sparkle_scale", text=tr("Scale"))
        layout.prop(sparkles_tool, "sparkle_detail", text=tr("Detail"))
        layout.prop(sparkles_tool, "sparkle_roughness", text=tr("Roughness"))
        
        layout.separator()
        layout.label(text=tr("Sparkle Color:"), icon='COLOR')
        layout.prop(sparkles_tool, "sparkle_color", text="")
        
        layout.separator()
        layout.operator("sparkles.create_sparkles", icon='ADD', text=tr("Create Sparkle Material"))

class VIEW3D_PT_gradient_editor(Panel):
    """Редактор градиентов"""
    bl_label = "Gradient Materials"
    bl_idname = "VIEW3D_PT_gradient_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "VIEW3D_PT_material_editor_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        gradient_tool = scene.gradient_tool
        
        layout.label(text=tr("Gradient Type:"), icon='MATERIAL')
        layout.prop(gradient_tool, "gradient_type", text="")
        
        layout.separator()
        layout.label(text=tr("Gradient Colors:"), icon='COLOR')
        
        layout.prop(gradient_tool, "use_three_colors", text=tr("Use Three Colors"))
        layout.prop(gradient_tool, "gradient_color1", text=tr("Color 1"))
        layout.prop(gradient_tool, "gradient_color2", text=tr("Color 2"))
        if gradient_tool.use_three_colors:
            layout.prop(gradient_tool, "gradient_color3", text=tr("Color 3"))
        
        layout.separator()
        layout.label(text=tr("Transformation:"), icon='ORIENTATION_GIMBAL')
        
        layout.prop(gradient_tool, "gradient_rotation", text=tr("Rotation"))
        layout.prop(gradient_tool, "gradient_scale", text=tr("Scale"))
        layout.prop(gradient_tool, "gradient_offset", text=tr("Offset"))
        
        layout.separator()
        layout.operator("gradient.create_gradient", icon='ADD', text=tr("Create Gradient Material"))

class VIEW3D_PT_alpha_tools(Panel):
    """Инструменты для работы с Alpha каналами"""
    bl_label = "Alpha Channel Tools"
    bl_idname = "VIEW3D_PT_alpha_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "VIEW3D_PT_material_editor_main"
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text=tr("Connect Alpha to BSDF:"), icon='TEXTURE')
        layout.operator("principled.connect_alpha_selected", text=tr("For Selected Objects"), icon='OBJECT_DATA')
        layout.operator("principled.connect_alpha_all", text=tr("For All Materials"), icon='WORLD')

# Классы для регистрации
classes = (
    AdvancedMaterialEditorPreferences,
    PrincipledProperties,
    PowderCoatingProperties,
    SparklesProperties,
    GradientProperties,
    PRINCIPLED_OT_update_materials,
    PRINCIPLED_OT_reset_values,
    PRINCIPLED_OT_copy_from_active,
    PRINCIPLED_OT_preset_metal,
    PRINCIPLED_OT_preset_plastic,
    PRINCIPLED_OT_preset_glass,
    PRINCIPLED_OT_preset_rubber,
    PRINCIPLED_OT_preset_ceramic,
    PRINCIPLED_OT_preset_wood,
    PRINCIPLED_OT_preset_powder_coating,
    PRINCIPLED_OT_connect_alpha_selected,
    PRINCIPLED_OT_connect_alpha_all,
    POWDER_OT_create_coating,
    SPARKLES_OT_create_sparkles,
    GRADIENT_OT_create_gradient,
    VIEW3D_PT_material_editor_main,
    VIEW3D_PT_basic_editor,
    VIEW3D_PT_powder_coating_editor,
    VIEW3D_PT_sparkles_editor,
    VIEW3D_PT_gradient_editor,
    VIEW3D_PT_alpha_tools,
)

def register():
    global current_language
    
    # Регистрируем переводы
    bpy.app.translations.register(__name__, translations_dict)
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.principled_tool = PointerProperty(type=PrincipledProperties)
    bpy.types.Scene.powder_coating_tool = PointerProperty(type=PowderCoatingProperties)
    bpy.types.Scene.sparkles_tool = PointerProperty(type=SparklesProperties)
    bpy.types.Scene.gradient_tool = PointerProperty(type=GradientProperties)
    
    # Устанавливаем язык по умолчанию
    prefs = bpy.context.preferences.addons.get(__name__)
    if prefs:
        current_language = prefs.preferences.language

def unregister():
    # Отменяем регистрацию переводов
    bpy.app.translations.unregister(__name__)
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.principled_tool
    del bpy.types.Scene.powder_coating_tool
    del bpy.types.Scene.sparkles_tool
    del bpy.types.Scene.gradient_tool

if __name__ == "__main__":
    register()