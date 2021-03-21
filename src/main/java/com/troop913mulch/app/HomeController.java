package com.troop913mulch.app;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.security.core.annotation.AuthenticationPrincipal;

@RestController
public class HomeController {

	@RequestMapping("/")
	public String index(@AuthenticationPrincipal User user) {
		return "Greetings from Spring Boot!";
	}

}
