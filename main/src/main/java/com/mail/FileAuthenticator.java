package com.mail;

import java.io.*;
import java.util.*;

/**
 * Gathers metadata from IMAP file and validates it against registration
 * information
 * Reports any offending/violating information
 */

public class FileAuthenticator {

    public static void main(String[] args) throws IOException {
        BufferedReader emailFileReader = new BufferedReader(new FileReader("inbox.txt"));
        BufferedReader csvFileReader = new BufferedReader(new FileReader("EmailChart.csv"));
        ArrayList<String> sheetSideEmails = new ArrayList<>();
        ArrayList<String> sheetSideNames = new ArrayList<>();
        Emails emails = new Emails();
        final int K_EMAIL_CHART_LENGTH = 53;

        String key = "";
        String value = "";

        for (long i = 0; i < 621; i++) {
            String throwawayString = emailFileReader.readLine();
            if (throwawayString != null) {
                // Grab address and other identifiers of sender, and standardize output
                if (throwawayString.startsWith("From: ")) {
                    value = throwawayString.substring(6, throwawayString.length()).toLowerCase().replace(" ", "");
                }
                // Grab address of reciever, ignore other identifiers
                if (throwawayString.startsWith("To: ")) {
                    if (throwawayString.contains(">")) {
                        int index = throwawayString.indexOf(">");
                        key = throwawayString.substring(4, index);
                    } else {
                        key = throwawayString.substring(4, throwawayString.length());
                    }

                    // Debugging: System.out.println(key + ", " + value);
                    // Write pairs into ArrayList
                    emails.addService(key, value);
                }
            }
        }
        // Close unnecessary readers and write to CSV
        emailFileReader.close();
        emails.writeToCSV("EmailsSent.csv");

        int index = 0;

        // Write and format registration information
        for (long i = 0; i < K_EMAIL_CHART_LENGTH; i++) {
            String throwawayString = csvFileReader.readLine();
            if (throwawayString != null) {
                index = throwawayString.indexOf(",");
                sheetSideEmails.add(
                        throwawayString.substring(index + 1, throwawayString.length()) + "@mail.cs-georgetown.net");
                sheetSideNames.add(throwawayString.substring(0, index).toLowerCase().replace(" ", ""));
            }
        }
        csvFileReader.close();

        int violations = 0;

        // Detect and report any violations by comparing services registerd for and
        // services currently emailing a given address
        for (int i = 0; i < sheetSideEmails.size(); i++) {
            ArrayList<String> x = emails.getServices(sheetSideEmails.get(i));
            for (int j = 0; j < x.size(); j++) {
                if (!x.get(j).contains(sheetSideNames.get(i))) {
                    System.out.println("Problem: " + x.get(j) + " is a service emailing " + sheetSideEmails.get(i)
                            + " without previously signing up.");
                    violations++;
                } else {
                    System.out.println("No problems yet for " + x.get(j) + " emailing " + sheetSideEmails.get(i));
                }
            }
        }
        System.out.println("Process finished with " + violations + " total violations.");
    }
}
