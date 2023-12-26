package com.my.app.springbootapp.trainning;

// import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;

@Component // this anotation makes this class as a bean and makes it ready for dpendency injection
// @Primary // to chose this bean class by default if multiple bean class is found, (Only one Primary bean class could be there)  
public class CricketCoach implements Coach {

    public CricketCoach(){
        System.out.println(" inside Constructor "+ getClass().getSimpleName());
    }


    // Example of bean life cycle
    @PostConstruct//to run my custom initialization after initialization of this class bean
    public void startupLogic(){
        System.out.println(" inside startupLogic "+ getClass().getSimpleName());
    }

    @PreDestroy// to run my own clean up logic befor class memory is cleaned
    public void cleanupLogic(){
        System.out.println(" inside cleanupLogic "+ getClass().getSimpleName());
    }

    @Override
    public String getDailyWorkOut() {
        return "Practice Bowling and Keeping :-)";
    }
    
}
