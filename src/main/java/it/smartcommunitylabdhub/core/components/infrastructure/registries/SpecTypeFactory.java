package it.smartcommunitylabdhub.core.components.infrastructure.registries;

import it.smartcommunitylabdhub.core.CoreApplication;
import it.smartcommunitylabdhub.core.annotations.SpecType;
import it.smartcommunitylabdhub.core.models.base.interfaces.Spec;
import jakarta.annotation.PostConstruct;
import lombok.extern.log4j.Log4j2;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.ClassPathScanningCandidateComponentProvider;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.core.type.filter.AnnotationTypeFilter;
import org.springframework.stereotype.Component;

import java.util.*;

@Log4j2
@Component
public class SpecTypeFactory {
    private final SpecRegistry<?> specRegistry;


    public SpecTypeFactory(SpecRegistry<?> specRegistry) {
        this.specRegistry = specRegistry;
    }

    @PostConstruct
    public void scanForSpecTypes() {
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();

        ClassPathScanningCandidateComponentProvider scanner = new ClassPathScanningCandidateComponentProvider(false);
        scanner.addIncludeFilter(new AnnotationTypeFilter(SpecType.class));

        List<String> basePackages = getBasePackages();  // Detect base package based on ComponentScan in CoreApplication

        Map<String, Class<? extends Spec>> specTypes = new HashMap<>();

        for (String basePackage : basePackages) {
            Set<BeanDefinition> candidateComponents = scanner.findCandidateComponents(basePackage);

            for (BeanDefinition beanDefinition : candidateComponents) {
                String className = beanDefinition.getBeanClassName();
                try {
                    Class<? extends Spec> specClass = (Class<? extends Spec>) Class.forName(className);
                    SpecType specTypeAnnotation = specClass.getAnnotation(SpecType.class);
                    specTypes.put(specTypeAnnotation.value(), specClass);
                } catch (ClassNotFoundException e) {
                    // Handle exceptions
                }
            }
        }

        specRegistry.registerSpecTypes(specTypes);
    }

    // Automatically detect the base packages using ComponentScan annotation
    private List<String> getBasePackages() {
        List<String> basePackages = new ArrayList<>();
        ComponentScan componentScan = CoreApplication.class.getAnnotation(ComponentScan.class);
        if (componentScan != null) {
            Collections.addAll(basePackages, componentScan.basePackages());
        }
        if (basePackages.isEmpty()) {
            throw new IllegalArgumentException("Base package not specified in @ComponentScan");
        }
        return basePackages;
    }
}
