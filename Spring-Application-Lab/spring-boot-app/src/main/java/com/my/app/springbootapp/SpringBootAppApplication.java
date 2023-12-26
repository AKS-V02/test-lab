package com.my.app.springbootapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// @SpringBootApplication(
// 	scanBasePackages = {"com.my.app.springbootapp",
// 						"com.my.app.util"}//use this when we need component scanning which is outside our default package
// )
@SpringBootApplication
public class SpringBootAppApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootAppApplication.class, args);
	}

}
