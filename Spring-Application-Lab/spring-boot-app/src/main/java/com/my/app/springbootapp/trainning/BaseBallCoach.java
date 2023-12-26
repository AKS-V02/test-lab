package com.my.app.springbootapp.trainning;

// import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Component;

@Component
// @Lazy // to create this bean only if it is required
public class BaseBallCoach implements Coach {

    public BaseBallCoach(){
        System.out.println(" inside Constructor "+ getClass().getSimpleName());
    }

    @Override
    public String getDailyWorkOut() {
        return "Practice batting !!!!";
    }
    
}
