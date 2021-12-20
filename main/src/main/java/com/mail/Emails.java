package com.mail;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * Basic class to store information on individual emails for processing
 * Service refers to companies emailing a given address
 * EmailAddress refers to a registered email address under the
 * domain @mail.cs-georgetown.net
 */

// TODO: Add timestamp/tracking capacity, and record other useful metadata

public class Emails {
    ArrayList<ArrayList<String>> m_services = new ArrayList<>();

    public Emails() {
        // Empty constructor
    }

    // Adds service linked with email address
    public void addService(String emailAddress, String service) {
        ArrayList<String> x = new ArrayList<>();

        x.add(emailAddress);
        x.add(service);
        m_services.add(x);
    }

    // Recalls all services associated with an emailAddress
    public ArrayList<String> getServices(String emailAddress) {
        ArrayList<String> x = new ArrayList<>();

        for (int i = 0; i < m_services.size(); i++) {
            if (m_services.get(i).get(0).equals(emailAddress)) {
                x.add(m_services.get(i).get(1));
            }
        }

        return x;
    }

    // Writes all valid data onto a csv file, recording information on every email
    public void writeToCSV(String csvPath) {
        try (PrintWriter writer = new PrintWriter(csvPath)) {
            
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < m_services.size(); i++) {
                sb.append(m_services.get(i).get(0));
                sb.append(',');
                sb.append(m_services.get(i).get(1));
                sb.append('\n');
            }
            writer.write(sb.toString());
            System.out.println("Successfully written to CSV");
            writer.close();

        } catch (FileNotFoundException e) {
            System.out.println(e.getMessage());
        }
    }
}
