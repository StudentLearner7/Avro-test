import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.query.Procedure;
import org.springframework.data.repository.query.Param;

public interface StoreProcExecutorRepository extends JpaRepository<Object, Long> {
    @Procedure
    void executeStoredProcedure1(@Param("inputParam1") String inputParam1, @Param("outputParam1") String outputParam1);

    @Procedure
    void executeStoredProcedure2(@Param("inputParam2") int inputParam2, @Param("outputParam2") int outputParam2);
}