import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class JacksonConfig {

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper objectMapper = new ObjectMapper();

        // Create a custom module for serialization configuration
        SimpleModule module = new SimpleModule();
        module.addSerializer(Object.class, new CustomResourceSerializer());

        objectMapper.registerModule(module);
        
        return objectMapper;
    }
}
___
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import org.springframework.hateoas.EntityModel;
import org.springframework.hateoas.Link;
import org.springframework.hateoas.server.LinkRelationProvider;
import org.springframework.hateoas.server.SimpleRepresentationModelAssembler;

import java.io.IOException;

public class CustomResourceSerializer extends JsonSerializer<Object> {

    private LinkRelationProvider relProvider;

    public CustomResourceSerializer(LinkRelationProvider relProvider) {
        this.relProvider = relProvider;
    }

    @Override
    public void serialize(Object value, JsonGenerator gen, SerializerProvider serializers) throws IOException {
        if (value instanceof EntityModel) {
            EntityModel<?> entityModel = (EntityModel<?>) value;

            // Serialize only the content without metadata
            gen.writeObject(entityModel.getContent());
        } else if (value instanceof SimpleRepresentationModelAssembler) {
            // Skip serializing SimpleRepresentationModelAssembler instances (for embedded resources)
        } else if (value instanceof Link) {
            Link link = (Link) value;

            // Serialize only the href of the link
            gen.writeStartObject();
            gen.writeStringField("href", link.getHref());
            gen.writeEndObject();
        } else {
            // Serialize other objects as is
            gen.writeObject(value);
        }
    }
}
