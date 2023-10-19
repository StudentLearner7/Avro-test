import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.concurrent.CountDownLatch;

@SpringBootTest
public class EmployeeControllerTest {
    @Autowired
    private EmployeeController employeeController;

    @Test
    public void testConcurrentUpdates() throws InterruptedException {
        int numColumns = 7;
        CountDownLatch latch = new CountDownLatch(numColumns);

        // Create an EmployeeDTO with initial data
        EmployeeDTO initialDTO = new EmployeeDTO();
        initialDTO.setFirstName("John");
        initialDTO.setLastName("Doe");
        // Set other fields...

        for (int i = 0; i < numColumns; i++) {
            // Create a copy of the initialDTO to modify a single field
            EmployeeDTO employeeDTO = new EmployeeDTO();
            employeeDTO.setFirstName(initialDTO.getFirstName());
            employeeDTO.setLastName(initialDTO.getLastName());
            // Set other fields...

            // Update a single column in a separate thread
            new Thread(() -> {
                employeeController.createOrUpdateEmployee(employeeDTO);
                latch.countDown();
            }).start();
        }

        // Wait for all threads to finish
        latch.await();
    }
}