import org.apache.maven.plugin.AbstractMojo;
import org.apache.maven.plugin.MojoExecutionException;
import org.apache.maven.plugins.annotations.Mojo;
import org.apache.maven.plugins.annotations.Parameter;
import org.apache.maven.project.MavenProject;
import org.apache.maven.shared.transfer.artifact.ArtifactCoordinate;
import org.codehaus.plexus.util.xml.Xpp3Dom;
import org.twdata.maven.mojoexecutor.MojoExecutor;

@Mojo(name = "generate-entities")
public class GenerateEntitiesMojo extends AbstractMojo {

    @Parameter(defaultValue = "${project}", readonly = true, required = true)
    private MavenProject project;

    @Parameter(defaultValue = "${session}", readonly = true, required = true)
    private org.apache.maven.execution.MavenSession session;

    public void execute() throws MojoExecutionException {
        try {
            // Define plugin coordinates
            String groupId = "org.hibernate";
            String artifactId = "hibernate-tools-maven-plugin";
            String version = "5.4.32.Final";

            // Define plugin goal
            String goal = "hbm2java";

            // Configure plugin
            Xpp3Dom configuration = MojoExecutor.configuration(
                    MojoExecutor.element("components",
                            MojoExecutor.element("component",
                                    MojoExecutor.element("name", "hbm2java"),
                                    MojoExecutor.element("implementation", "org.hibernate.tool.maven.Hbm2JavaMojo"),
                                    MojoExecutor.element("outputDirectory", "target/generated-sources/hibernate"),
                                    MojoExecutor.element("templatePath", "src/main/resources/templates"),
                                    MojoExecutor.element("ejb3", "true")
                            )
                    )
            );

            // Execute plugin
            MojoExecutor.executeMojo(
                    MojoExecutor.plugin(groupId, artifactId, version),
                    MojoExecutor.goal(goal),
                    configuration,
                    MojoExecutor.executionEnvironment(project, session, pluginManager)
            );
        } catch (Exception e) {
            throw new MojoExecutionException("Failed to execute plugin", e);
        }
    }
}
