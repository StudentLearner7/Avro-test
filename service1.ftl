package com.your.package.service;

import com.your.package.dto.${entityName}DTO;
import com.your.package.entities.${entityName};
import com.your.package.repository.${entityName}Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ${entityName}Service {

    @Autowired
    private ${entityName}Repository repository;

    // DTO to Entity conversion
    private ${entityName} toEntity(${entityName}DTO dto) {
        ${entityName} entity = new ${entityName}();
<#list fields as field>
        entity.set${field.name?cap_first}(dto.get${field.name?cap_first}());
</#list>
        return entity;
    }

    // Entity to DTO conversion
    private ${entityName}DTO toDTO(${entityName} entity) {
        ${entityName}DTO dto = new ${entityName}DTO();
<#list fields as field>
        dto.set${field.name?cap_first}(entity.get${field.name?cap_first}());
</#list>
        return dto;
    }

    public List<${entityName}DTO> findAll() {
        return repository.findAll().stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    public ${entityName}DTO findById(Long id) {
        return repository.findById(id)
            .map(this::toDTO)
            .orElse(null);
    }

    public ${entityName}DTO save(${entityName}DTO dto) {
        return toDTO(repository.save(toEntity(dto)));
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
