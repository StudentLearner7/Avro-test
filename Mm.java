
import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.junit4.SpringRunner;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

@RunWith(SpringRunner.class)
@DataJpaTest
public class UserServiceTest {

    @Autowired
    private UserRepository userRepository;

    private UserService userService;

    @Before
    public void setUp() {
        userService = new UserService();
        userService.setUserRepository(userRepository);
    }

    @Test
    public void testCreateAndFindUser() {
        User user = new User();
        user.setName("John Doe");

        User createdUser = userService.createUser(user);
        assertNotNull(createdUser);
        assertNotNull(createdUser.getId());

        User foundUser = userService.findUserById(createdUser.getId());
        assertEquals(createdUser.getName(), foundUser.getName());
    }
}