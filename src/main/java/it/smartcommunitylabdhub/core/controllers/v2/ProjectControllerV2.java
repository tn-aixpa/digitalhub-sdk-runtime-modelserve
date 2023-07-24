package it.smartcommunitylabdhub.core.controllers.v2;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import it.smartcommunitylabdhub.core.annotations.ApiVersion;

// TODO: put as example in documentation.
@RestController
@RequestMapping("/projects")
@ApiVersion("v2")
public class ProjectControllerV2 {

    @GetMapping(produces = "text/plain", consumes = "text/plain", path = "/json1")
    @ResponseBody
    public String myVersioned2Json() {
        return "hello I'm a string V2";
    }

}
