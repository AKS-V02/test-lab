package com.my.app.springbootapp.trainning;

// import org.springframework.beans.factory.config.ConfigurableBeanFactory;
// import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
//to set the scope for the bean created by spring
// @Scope(ConfigurableBeanFactory.SCOPE_SINGLETON) // (only one instace is created and shared for all reference)
// @Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE) // (create instance for each injection)
public class TrackCoach implements Coach {

    public TrackCoach(){
        System.out.println(" inside Constructor "+ getClass().getSimpleName());
    }

    @Override
    public String getDailyWorkOut() {
        return "Practice Running!!!";
    }
    
}
