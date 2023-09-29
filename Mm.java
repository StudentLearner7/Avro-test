// Inside the visit method for MethodDeclaration
@Override
public void visit(MethodDeclaration md, Void arg) {
    super.visit(md, arg);

    // Check if the method has a @OneToMany annotation
    md.getAnnotationByName("OneToMany").ifPresent(annotationExpr -> {
        // Check if the annotation has a value for "fetch" and it's set to "FetchType.LAZY"
        annotationExpr.ifSingleMemberAnnotationExpr(singleMember -> {
            if (singleMember.getMemberValue().asString().equals("FetchType.LAZY")) {
                // Modify the annotation to set fetchType to FetchType.EAGER
                singleMember.replace(ExpressionParser.parseExpression("FetchType.EAGER"));
                
                // Add import statements for FetchType and CascadeType if needed
                addImportStatement(md.findCompilationUnit(), "javax.persistence.FetchType");
                addImportStatement(md.findCompilationUnit(), "javax.persistence.CascadeType");
            }
        });

        // Add cascade type "CascadeType.ALL" if not already present
        annotationExpr.ifNormalAnnotationExpr(normalAnnotation -> {
            if (!normalAnnotation.getPairs().stream().anyMatch(pair ->
                    pair.getNameAsString().equals("cascade") &&
                    pair.getValue().asString().equals("CascadeType.ALL"))) {
                normalAnnotation.addPair("cascade", "CascadeType.ALL");
            }
        });

        // Add orphan removal "true" if not already present
        annotationExpr.ifNormalAnnotationExpr(normalAnnotation -> {
            if (!normalAnnotation.getPairs().stream().anyMatch(pair ->
                    pair.getNameAsString().equals("orphanRemoval") &&
                    pair.getValue().asBooleanLiteralExpr().getValue())) {
                normalAnnotation.addPair("orphanRemoval", "true");
            }
        });
    });
}