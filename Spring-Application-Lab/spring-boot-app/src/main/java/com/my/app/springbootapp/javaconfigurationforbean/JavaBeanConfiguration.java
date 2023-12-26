package com.my.app.springbootapp.javaconfigurationforbean;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.my.app.springbootapp.trainning.Coach;
import com.my.app.springbootapp.trainning.SwimCoach;

// java bean configuration example
// use case: to make third party classes or classes whose code is not accesible, available for Spring framwork to create bean
@Configuration
public class JavaBeanConfiguration {
    
    @Bean // bean created with this method name
    public Coach newSwimCoach(){
        return new SwimCoach();
    }
    
}
