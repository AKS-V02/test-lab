package com.my.lab;

import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Instant;
import java.time.LocalDate;
import java.time.Month;
import java.time.ZoneId;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.StringJoiner;
import java.util.TimeZone;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import java.util.zip.ZipFile;

import javax.script.ScriptEngine;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( "Hello World!" );
        System.out.println(Arrays.toString(twoSum(new int[]{3,2,4}, 6)));
        List<Student> elist = List
                    .of(new Student("Stenny", 24),
                    new Student("Rucha", 22),
                    new Student("Vihaan", 21),
                    new Student("Stenny", 22)    
                    );
        Map<String, Integer> map = elist.stream()
        .collect(Collectors.toMap(Student::getName, 
                        Student::getAge,
                        (oldV, newV)->oldV));
        System.out.println(map);
        
        // elist.forEach(consumerWrappre(num->System.out.println(""),ArithmeticException.class));

        // String fileName = "c://Sample.txt";

        // try(Stream<String> stream = Files.lines(Paths.get(fileName))){
        //     stream.forEach(System.out::println);
        // } catch (Exception e) {
        //     // TODO: handle exception
        // }

        StringJoiner jr1 = new StringJoiner("delimeter", "pre", "suf");
        jr1.merge(jr1);

        Set<Integer> intSet = new HashSet<>();
        intSet.add(47);
        intSet.forEach(System.out::println);

        LocalDate date = LocalDate.of(2019, Month.MARCH, 30);
        LocalDate date2 = LocalDate.ofYearDay(2020, 255);
        LanguageService ll = message -> System.out.println("ff"+message);
        ll.showMassage("ff");

        // Calculator sum = (int sum)-> a+b;
        // int a = sum.add(4,5);


        double radiu = 4.55;
        Circle circle = (double radius)->3.14*radius*radius;
        circle.calculateArea(radiu);

        List<String> data = Arrays.asList("ss","wws","rr");
        List<String> sortedData = data.stream()
                .sorted((s1,s2)->s1.compareTo(s2)).collect(Collectors.toList());
        System.out.println("sorted "+sortedData);
        List<String> sortedData2 = data.stream()
                .sorted(String::compareTo).collect(Collectors.toList());
        System.out.println("sorted2 "+sortedData2);
        
        
        App x = new App();
        myInte obj = x.new Myclass();
        obj.name();

        Optional<Integer> op = Optional.ofNullable(null);

        // double dd = data.stream().collect(Collectors.averagingInt(null));

        Stream<Student> st = elist.stream().filter(stu->stu.getName().equalsIgnoreCase("kk"));

        final Calendar calendar = new Calendar.Builder().setInstant(Instant.now().toEpochMilli())
                                .setTimeZone(TimeZone.getTimeZone(ZoneId.systemDefault())).setLocale(Locale.getDefault()).build();

        System.out.println("Time "+ Instant.ofEpochMilli(Instant.now().toEpochMilli()));

        List<Integer> integersList = IntStream.range(1, 10).boxed()
            .collect(Collectors.toCollection(ArrayList::new));
        System.out.println("intiger list"+integersList);

        // System.out.println(lengthOfLongestSubstring("pwwkew"));
        System.out.println(merge(new int[] {1,2,2,3},new int[] {2,4,5,6}));
    }

    public void printEntries(PrintStream stream, String zip){
        try (ZipFile zipFile = new ZipFile(zip)){
            zipFile.stream().forEach(stream::println);
        } catch (Exception e) {
            // TODO: handle exception
        }
    }

    public static int[] merge(int[] n1, int[] n2){
        int l = n1.length+ n2.length;
        int[] r = new int[l];
        int j = 0;
        int k = 0;
        for(int i=0; i<l; i++){
            if(j< n1.length && k<n2.length){
                if(n1[j]>n2[k]){
                    r[i] = n2[k];
                    k++;
                }else{
                    r[i] = n1[j];
                    j++;
                }
            }else if(j<n1.length){
                r[i] = n1[j];
                j++;
            }else if(k<n2.length){
                r[i] = n2[k];
                k++;
            }
            System.out.println("r[i] "+r[i]);
        }
        return r;
    }
    public double sortedArrayMedian(int[] num){
        int i = (num.length/2);
        if((num.length%2) == 0){
            return (num[i] + num[i-1])/2;
        }else{
            return num[i];
        }
    }

    public double mergedSortedArrayMedian(int[] n1, int[] n2){
        int l = n1.length+ n2.length;
        int m = (l/2);
        int[] r = new int[m+1];
        int j = 0;
        int k = 0;
        for(int i=0; i<=m; i++){
            if(j< n1.length && k<n2.length){
                if(n1[j]>n2[k]){
                    r[i] = n2[k];
                    k++;
                }else{
                    r[i] = n1[j];
                    j++;
                }
            }else if(j<n1.length){
                r[i] = n1[j];
                j++;
            }else if(k<n2.length){
                r[i] = n2[k];
                k++;
            }
            if(i==m){
                if((l%2) == 0){
                    double a = (r[i] + r[i-1]);
                    return a/2;
                }else{
                    return r[i];
                }
            }
        }
        return 0;
    }

    public String longestPalindrome(String s) {
        String r = s.length()>0? s.substring(0, 1): "";

        for(int i=0; i< s.length(); i++){
            int d = 1;
            if(i>0 && i+d< s.length() && s.charAt(i-d) == s.charAt(i+d)){
                
                do {
                    d++;
                }while((i-d) >= 0 && (i+d)<s.length() && s.charAt(i-d) == s.charAt(i+d));

                d--;
                if(r.length()<((2*d)+1)){
                    r = s.substring((i-d), (i+d+1));
                }
                i = i+d;
            }else if( i+d< s.length() && s.charAt(i) == s.charAt(i+d)){
                do {
                    d++;
                } while((i+1-d) > 0 && (i+d)<s.length() && s.charAt(i+1-d) == s.charAt(i+d));
                d--;
                if(r.length()<(2*d)){
                    r = s.substring((i+1-d), (i+d+1));
                }
                i = i+d;
            }
        }

        return r;
    }

    public static int lengthOfLongestSubstring(String s) {
        if (s.length() < 2)
            return s.length();
        int start = 0;
        int end = 0;
        int r = 0;
        for (char c : s.toCharArray()) {
            for(int i = start; i<end; i++){
               start =  (s.charAt(i) == c) ? i+1 : start; 
            }
            if((end-start)> r){
                r = (end-start);
            }
            end++;
        }
        return r+1;
    }


    // public int lengthOfLongestSubstring(String s) {
    //     if (s.length() < 2)
    //         return s.length();
    //     int r = 0;
    //     StringBuilder sb = new StringBuilder();
    //     for (char c : s.toCharArray()) {
    //         for (int i = 0; i < sb.length(); i++) {
    //             if (c == sb.charAt(i)) {
    //                 if (r < sb.length()) {
    //                     r = sb.length();
    //                 }
    //                 sb.delete(0, (i + 1));
    //             }
    //         }
    //         sb.append(c);
    //     }
    //     if (r < sb.length()) {
    //         r = sb.length();
    //     }
    //     return r;
    // }

    public static int[] twoSum(int[] nums, int target) {
        if(nums.length==2) return new int[] { 0, 1 };
        Map<Integer, Integer> a = new HashMap<>();
        for(int i=0 ; i<nums.length ; i++){
            if(a.containsKey(nums[i])){
                return new int[]{ a.get(nums[i]), i };
            }
            a.putIfAbsent((target-nums[i]), i);
        }
        return new int[]{};
    }

    // public static int[] twoSum(int[] nums, int target) {
    //     if(nums.length==2) return new int[] { 0, 1 };
    //     for(int i=0 ; i<nums.length ; i++){
    //         int b = (target-nums[i]);
    //         for(int j=i+1; j<nums.length; j++ ){
    //             if(b==nums[j]){
    //                 return new int[]{ i, j };
    //             }
    //         }
    //     }
    //     return new int[]{};
    // }

    interface myInte{
        default void name() {
            System.out.println("myInterface");
        }
    }

    class Myclass implements myInte{
        public void name(){
            System.out.println("my class");
        }
    }
    
    
    
    @FunctionalInterface
    public interface Circle{
        double calculateArea(double radius);
    }

    // @FunctionalInterface
    // public interface Calculator{
    //     int add(int a, int b);
    //     int multiply(int a, int b);
    // }
    interface LanguageService{
        void showMassage(String message);
    }

    static <T,E extends Exception> Consumer<T> 
                        consumerWrappre(Consumer<T> consumer, Class<E> clazz){
                            return num ->{
                                try {
                                    consumer.accept(num);
                                } catch (Exception e) {
                                    E exCast = clazz.cast(e);
                                    System.err.println("exception "+exCast.getMessage());
                                }
                            };
    }
}
