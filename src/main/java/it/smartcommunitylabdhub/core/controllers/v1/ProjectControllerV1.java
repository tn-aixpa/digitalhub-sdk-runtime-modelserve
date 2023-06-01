package it.smartcommunitylabdhub.core.controllers.v1;

import java.util.List;

import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylabdhub.core.annotations.ApiVersion;
import it.smartcommunitylabdhub.core.annotations.ValidName;
import it.smartcommunitylabdhub.core.models.dtos.ArtifactDTO;
import it.smartcommunitylabdhub.core.models.dtos.FunctionDTO;
import it.smartcommunitylabdhub.core.models.dtos.ProjectDTO;
import it.smartcommunitylabdhub.core.models.dtos.WorkflowDTO;
import it.smartcommunitylabdhub.core.services.interfaces.ProjectService;

@RestController
@RequestMapping("/projects")
@ApiVersion("v1")
@Validated
public class ProjectControllerV1 {

    private final ProjectService projectService;

    public ProjectControllerV1(ProjectService projectService) {
        this.projectService = projectService;
    }

    @GetMapping(path = "", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<ProjectDTO>> getProjects(Pageable pageable) {
        return ResponseEntity.ok(this.projectService.getProjects(pageable));
    }

    @PostMapping(value = "", consumes = { MediaType.APPLICATION_JSON_VALUE, "application/x-yaml" })
    public ResponseEntity<ProjectDTO> createProject(@RequestBody ProjectDTO projectDTO) {
        return ResponseEntity.ok(this.projectService.createProject(projectDTO));
    }

    @GetMapping(path = "/{uuid}", produces = "application/json; charset=UTF-8")
    public ResponseEntity<ProjectDTO> getProject(@ValidName @PathVariable(name = "uuid", required = true) String uuid) {
        return ResponseEntity.ok(this.projectService.getProject(uuid));
    }

    @PutMapping(path = "/{uuid}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/x-yaml" }, produces = "application/json")
    public ResponseEntity<ProjectDTO> updateProject(
            @RequestBody ProjectDTO projectDTO,
            @ValidName @PathVariable String uuid) {
        return ResponseEntity.ok(this.projectService.updateProject(projectDTO, uuid));
    }

    @DeleteMapping(path = "/{name}")
    public ResponseEntity<Boolean> deleteProject(@ValidName @PathVariable String name) {
        return ResponseEntity.ok(this.projectService.deleteProjectByName(name));
    }

    @GetMapping(path = "/{uuid}/functions", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<FunctionDTO>> projectFunctions(@ValidName @PathVariable String uuid) {
        return ResponseEntity.ok(this.projectService.getProjectFunctions(uuid));
    }

    @GetMapping(path = "/{uuid}/workflows", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<WorkflowDTO>> projectWorkflows(@ValidName @PathVariable String uuid) {
        return ResponseEntity.ok(this.projectService.getProjectWorkflows(uuid));
    }

    @GetMapping(path = "/{uuid}/artifacts", produces = "application/json; charset=UTF-8")
    public ResponseEntity<List<ArtifactDTO>> projectArtifacts(@ValidName @PathVariable String uuid) {
        return ResponseEntity.ok(this.projectService.getProjectArtifacts(uuid));
    }

}
