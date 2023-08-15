import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ${entityName}Service {

    private final ${entityName}Repository ${entityName?uncap_first}Repository;

    @Autowired
    public ${entityName}Service(${entityName}Repository ${entityName?uncap_first}Repository) {
        this.${entityName?uncap_first}Repository = ${entityName?uncap_first}Repository;
    }

    public List<${entityName}DTO> findAll() {
        // You might need to convert entity to DTO
        return ${entityName?uncap_first}Repository.findAll();
    }

    public ${entityName}DTO findById(Long id) {
        // Convert entity to DTO
        return ${entityName?uncap_first}Repository.findById(id).orElse(null);
    }

    public ${entityName}DTO save(${entityName}DTO ${entityName?uncap_first}DTO) {
        // Convert DTO to entity and save
        return ${entityName?uncap_first}Repository.save(${entityName?uncap_first}DTO);
    }

    public void delete(Long id) {
        ${entityName?uncap_first}Repository.deleteById(id);
    }
    
    // Additional CRUD methods...
}
