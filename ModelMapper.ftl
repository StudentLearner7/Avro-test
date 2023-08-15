public class ModelMapper {

<#list entities as entity>
    public static ${entity.name} toEntity(${entity.name}DTO dto) {
        if (dto == null) {
            return null;
        }
        
        ${entity.name} entity = new ${entity.name}();
<#list entity.fields as field>
    <#if field.isPrimitive>
        entity.set${field.name?cap_first}(dto.get${field.name?cap_first}());
    <#else>
        entity.set${field.name?cap_first}(toEntity(dto.get${field.name?cap_first}()));
    </#if>
</#list>
        return entity;
    }

    public static ${entity.name}DTO toDTO(${entity.name} entity) {
        if (entity == null) {
            return null;
        }

        ${entity.name}DTO dto = new ${entity.name}DTO();
<#list entity.fields as field>
    <#if field.isPrimitive>
        dto.set${field.name?cap_first}(entity.get${field.name?cap_first}());
    <#else>
        dto.set${field.name?cap_first}(toDTO(entity.get${field.name?cap_first}()));
    </#if>
</#list>
        return dto;
    }

</#list>
}
