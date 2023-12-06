@Aspect
@Component
public class ExceptionHandlingAspect {

    @AfterThrowing(pointcut = "execution(* com.yourapp..*.*(..))", throwing = "ex")
    public void handleAllThrowable(Throwable ex) {
        // Log the issue or alert, but generally don't attempt recovery from Errors
    }
}