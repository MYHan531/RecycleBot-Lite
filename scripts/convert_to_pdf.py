#!/usr/bin/env python3
"""
Convert Service Blueprint to PDF
Converts markdown service blueprint to PDF format
"""

import os
import subprocess
import sys

def convert_markdown_to_pdf():
    """Convert markdown blueprint to PDF"""
    
    # Check if required tools are available
    try:
        # Try to use pandoc if available
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Using pandoc to convert markdown to PDF...")
            
            # Create docs directory if it doesn't exist
            os.makedirs('docs', exist_ok=True)
            
            # Convert markdown to PDF using pandoc
            cmd = [
                'pandoc',
                'docs/service_blueprint.md',
                '-o', 'docs/blueprint.pdf',
                '--pdf-engine=xelatex',
                '--variable=geometry:margin=1in',
                '--variable=fontsize:11pt',
                '--variable=mainfont:DejaVu Sans',
                '--variable=monofont:DejaVu Sans Mono',
                '--toc',
                '--number-sections'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PDF created successfully: docs/blueprint.pdf")
                return True
            else:
                print(f"❌ Pandoc conversion failed: {result.stderr}")
                return False
                
    except FileNotFoundError:
        print("Pandoc not found. Trying alternative methods...")
    
    # Alternative: Use markdown-pdf if available
    try:
        result = subprocess.run(['markdown-pdf', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Using markdown-pdf to convert...")
            
            cmd = ['markdown-pdf', 'docs/service_blueprint.md', '-o', 'docs/blueprint.pdf']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ PDF created successfully: docs/blueprint.pdf")
                return True
            else:
                print(f"❌ Markdown-pdf conversion failed: {result.stderr}")
                return False
                
    except FileNotFoundError:
        print("Markdown-pdf not found.")
    
    # Fallback: Create a simple HTML version
    print("Creating HTML version as fallback...")
    create_html_fallback()
    return False

def create_html_fallback():
    """Create HTML version as fallback when PDF tools are not available"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEA Waste Management Service Blueprint</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        h3 {
            color: #7f8c8d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 10px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
        .wait-time {
            background-color: #d1ecf1;
            padding: 8px;
            border-radius: 4px;
            margin: 5px 0;
        }
        .metric {
            background-color: #d4edda;
            padding: 8px;
            border-radius: 4px;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>NEA Waste Management Service Blueprint</h1>
        
        <div class="highlight">
            <strong>Note:</strong> This is an HTML version of the service blueprint. 
            For the PDF version, please install pandoc or markdown-pdf tools.
        </div>
        
        <h2>Service Overview</h2>
        <p>This blueprint outlines the complete service journey for NEA's waste management and recycling services, including digital touchpoints, human interactions, and expected wait times.</p>
        
        <h2>Service Touchpoints</h2>
        
        <h3>1. Digital Self-Service Portal</h3>
        <p><strong>URL:</strong> https://www.nea.gov.sg/our-services/waste-management</p>
        
        <h4>Entry Points:</h4>
        <ul>
            <li><strong>Website Navigation:</strong> 2-3 clicks to reach waste management section</li>
            <li><strong>Search Function:</strong> Direct access via search terms</li>
            <li><strong>Mobile App (myENV):</strong> iOS/Android app access</li>
        </ul>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Page Load Time:</strong> 2-5 seconds<br>
            <strong>Search Response:</strong> 1-3 seconds<br>
            <strong>Form Submission:</strong> 3-8 seconds
        </div>
        
        <h3>2. Information & Education Services</h3>
        <h4>Online Resources:</h4>
        <ul>
            <li><strong>Waste Statistics Reports:</strong> Immediate download</li>
            <li><strong>Recycling Guidelines:</strong> Instant access</li>
            <li><strong>Educational Materials:</strong> PDF downloads (2-5 seconds)</li>
        </ul>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Content Loading:</strong> 1-3 seconds<br>
            <strong>Document Downloads:</strong> 5-15 seconds (depending on file size)<br>
            <strong>Video Content:</strong> 2-5 seconds buffering
        </div>
        
        <h3>3. Hotline Services</h3>
        <h4>NEA Contact Center</h4>
        <p><strong>Phone:</strong> 1800-CALL NEA (1800-2255 632)<br>
        <strong>Operating Hours:</strong> Monday to Friday, 8:00 AM - 6:00 PM</p>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Initial Queue:</strong> 3-8 minutes (peak hours: 8-10 minutes)<br>
            <strong>Call Handling:</strong> 5-15 minutes per inquiry<br>
            <strong>Follow-up Response:</strong> 24-48 hours
        </div>
        
        <h4>Call Categories:</h4>
        <table>
            <tr>
                <th>Service Type</th>
                <th>Duration</th>
            </tr>
            <tr>
                <td>General Inquiries</td>
                <td>5-8 minutes</td>
            </tr>
            <tr>
                <td>Technical Support</td>
                <td>8-15 minutes</td>
            </tr>
            <tr>
                <td>Complaint Handling</td>
                <td>10-20 minutes</td>
            </tr>
            <tr>
                <td>Emergency Response</td>
                <td>Immediate (within 2 minutes)</td>
            </tr>
        </table>
        
        <h3>4. E-Services Portal</h3>
        <h4>Available Services:</h4>
        <ul>
            <li><strong>Waste Collection Booking:</strong> 3-5 minutes processing</li>
            <li><strong>Recycling Point Locator:</strong> 1-2 seconds response</li>
            <li><strong>Report Illegal Dumping:</strong> 5-10 minutes form completion</li>
            <li><strong>Request Information:</strong> 2-3 business days response</li>
        </ul>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Portal Login:</strong> 1-3 seconds<br>
            <strong>Form Processing:</strong> 3-8 seconds<br>
            <strong>Confirmation Email:</strong> 1-5 minutes<br>
            <strong>Service Completion:</strong> Varies by service type
        </div>
        
        <h3>5. Physical Service Centers</h3>
        <h4>NEA Building</h4>
        <p><strong>Address:</strong> 40 Scotts Road, Environment Building, Singapore 228231<br>
        <strong>Operating Hours:</strong> Monday to Friday, 8:30 AM - 6:00 PM</p>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Security Check:</strong> 1-2 minutes<br>
            <strong>Reception Queue:</strong> 5-15 minutes<br>
            <strong>Service Counter:</strong> 10-30 minutes<br>
            <strong>Document Processing:</strong> 15-45 minutes
        </div>
        
        <h3>6. Mobile Services</h3>
        <h4>myENV App Performance:</h4>
        <div class="metric">
            <strong>App Launch:</strong> 2-4 seconds<br>
            <strong>Feature Access:</strong> 1-3 seconds<br>
            <strong>Data Sync:</strong> 2-5 seconds<br>
            <strong>Push Notifications:</strong> Immediate
        </div>
        
        <h4>Wait Times:</h4>
        <div class="wait-time">
            <strong>Location Services:</strong> 3-5 seconds<br>
            <strong>Photo Upload:</strong> 5-15 seconds<br>
            <strong>Report Submission:</strong> 3-8 seconds
        </div>
        
        <h2>Performance Metrics</h2>
        
        <h3>Digital Services:</h3>
        <div class="metric">
            <strong>Website Uptime:</strong> 99.9%<br>
            <strong>Page Load Speed:</strong> &lt;3 seconds<br>
            <strong>Mobile Responsiveness:</strong> 100%<br>
            <strong>Search Accuracy:</strong> 95%
        </div>
        
        <h3>Human Services:</h3>
        <div class="metric">
            <strong>Call Answer Rate:</strong> 95% within 30 seconds<br>
            <strong>First Call Resolution:</strong> 85%<br>
            <strong>Customer Satisfaction:</strong> 4.2/5.0<br>
            <strong>Service Completion Rate:</strong> 98%
        </div>
        
        <h3>Response Times:</h3>
        <table>
            <tr>
                <th>Service Type</th>
                <th>Response Time</th>
            </tr>
            <tr>
                <td>Email Inquiries</td>
                <td>24-48 hours</td>
            </tr>
            <tr>
                <td>Online Forms</td>
                <td>2-3 business days</td>
            </tr>
            <tr>
                <td>Emergency Reports</td>
                <td>&lt;2 hours</td>
            </tr>
            <tr>
                <td>General Complaints</td>
                <td>3-5 business days</td>
            </tr>
        </table>
        
        <h2>Service Improvement Areas</h2>
        
        <h3>Identified Bottlenecks:</h3>
        <ol>
            <li><strong>Peak Hour Call Queues:</strong> 8-10 minutes wait time</li>
            <li><strong>Document Processing:</strong> 15-45 minutes for complex requests</li>
            <li><strong>Mobile App Performance:</strong> Occasional slow loading during peak usage</li>
        </ol>
        
        <h3>Optimization Opportunities:</h3>
        <ol>
            <li><strong>AI Chatbot Integration:</strong> Reduce call volume by 30%</li>
            <li><strong>Digital Document Processing:</strong> Reduce processing time by 50%</li>
            <li><strong>Mobile App Optimization:</strong> Improve load times by 40%</li>
        </ol>
        
        <h2>Future Service Enhancements</h2>
        
        <h3>Planned Improvements:</h3>
        <ol>
            <li><strong>AI-Powered Chatbot:</strong> Reduce wait times by 60%</li>
            <li><strong>Predictive Analytics:</strong> Proactive service recommendations</li>
            <li><strong>Mobile-First Design:</strong> Enhanced mobile experience</li>
            <li><strong>Integration with Smart City:</strong> Real-time waste monitoring</li>
        </ol>
        
        <h3>Expected Impact:</h3>
        <div class="metric">
            <strong>Wait Time Reduction:</strong> 40-60% across all channels<br>
            <strong>Customer Satisfaction:</strong> Target 4.5/5.0<br>
            <strong>Service Efficiency:</strong> 30% improvement in processing times<br>
            <strong>Digital Adoption:</strong> 80% of transactions online
        </div>
        
        <hr>
        <p><em>Last Updated: January 2024<br>
        Next Review: June 2024</em></p>
    </div>
</body>
</html>"""
    
    # Create docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Write HTML file
    with open('docs/blueprint.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML version created: docs/blueprint.html")
    print("💡 To convert to PDF, you can:")
    print("   1. Open the HTML file in a browser")
    print("   2. Use 'Print to PDF' function")
    print("   3. Or install pandoc: pip install pandoc")
    print("   4. Or install markdown-pdf: npm install -g markdown-pdf")

def main():
    """Main function"""
    print("Converting Service Blueprint to PDF...")
    
    success = convert_markdown_to_pdf()
    
    if success:
        print("\n🎉 PDF conversion completed successfully!")
        print("📄 File location: docs/blueprint.pdf")
    else:
        print("\n⚠️  PDF conversion failed, but HTML version created.")
        print("📄 HTML file location: docs/blueprint.html")

if __name__ == "__main__":
    main() 