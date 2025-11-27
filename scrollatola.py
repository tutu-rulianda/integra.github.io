def get_fixed_scroll_and_title_js():
    """Fixed scroll button and proper title positioning in modal"""
    return """
    function() {
        console.log('=== FIXED SCROLL + PROPER TITLE ===');

        // 1. Remove any existing scroll button first
        const oldScrollBtn = document.getElementById('scrollTopBtn');
        if (oldScrollBtn) oldScrollBtn.remove();

        // 2. FIXED SCROLL BUTTON - Use absolute positioning and direct event
        const scrollBtn = document.createElement('button');
        scrollBtn.id = 'scrollTopBtn';
        scrollBtn.innerHTML = '↑';
        scrollBtn.title = 'Back to Top';
        scrollBtn.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: #333;
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
            z-index: 1000002; /* Higher than modal */
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            opacity: 0.9;
            transition: all 0.3s ease;
            display: none; /* Initially invisible */
        `;

        // Track the last scrolled element to know what to scroll back up
        let lastScrolledContainer = window;

        // DIRECT CLICK HANDLER - No event delegation for scroll button
        scrollBtn.addEventListener('click', function(e) {
            console.log('🎯 Scroll button clicked directly');
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            // 1. Scroll the last detected container
            if (lastScrolledContainer && lastScrolledContainer.scrollTo) {
                try {
                    lastScrolledContainer.scrollTo({ top: 0, behavior: 'smooth' });
                } catch (err) {
                    // Fallback for elements that might not support scrollTo options
                    lastScrolledContainer.scrollTop = 0;
                }
            }

            // 2. Scroll standard window/body targets just in case
            window.scrollTo({ top: 0, behavior: 'smooth' });
            document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
            document.body.scrollTo({ top: 0, behavior: 'smooth' });
            
            // 3. Try to find Gradio container explicitly
            const gradioContainer = document.querySelector('.gradio-container');
            if (gradioContainer) {
                gradioContainer.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });

        document.body.appendChild(scrollBtn);
        console.log('✅ Fixed scroll button added with z-index: 1000002');

        // GLOBAL CAPTURE SCROLL LISTENER
        // This catches scroll events on ANY element in the DOM
        window.addEventListener('scroll', function(e) {
            const target = e.target;
            
            // Determine scroll position based on target type
            let scrollTop = 0;
            
            if (target === document) {
                scrollTop = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                lastScrolledContainer = window;
            } else if (target instanceof Element) {
                scrollTop = target.scrollTop;
                lastScrolledContainer = target;
            }

            // Show/Hide button
            if (scrollTop > 100) {
                scrollBtn.style.display = 'block';
            } else {
                scrollBtn.style.display = 'none';
            }
        }, { capture: true, passive: true });

        // 3. CSS with proper title positioning
        const style = document.createElement('style');
        style.textContent = `
            html, body { 
                scroll-behavior: smooth !important; 
            }

            /* MODAL WITH PROPER TITLE POSITIONING */
            .fixed-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.95);
                z-index: 1000000;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                overflow-y: auto;
                padding: 40px 20px;
            }

            .fixed-modal-content {
                position: relative;
                max-width: 90%;
                margin: 40px auto;
                text-align: center;
            }

            .fixed-modal img {
                max-width: 100%;
                max-height: calc(100vh - 120px);
                width: auto;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.7);
                object-fit: contain;
                display: block;
            }

            /* PROPER TITLE POSITIONING - Inside the image area */
            .fixed-modal-title {
                position: absolute;
                top: 15px; /* Position from top of the image */
                right: 15px; /* Position from right of the image */
                color: white;
                background: rgba(0,0,0,0.8);
                padding: 8px 16px;
                border-radius: 20px;
                font-family: system-ui, sans-serif;
                font-size: 14px;
                font-weight: 600;
                z-index: 1000002;
                backdrop-filter: blur(5px);
                border: 1px solid rgba(255,255,255,0.2);
            }

            /* PERFECT CIRCLE CLOSE BUTTON */
            .fixed-modal-close {
                position: fixed;
                top: 50px;
                left: 50px;
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                cursor: pointer;
                font-size: 20px;
                font-weight: bold;
                z-index: 1000001;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                transition: all 0.2s ease;
            }

            .fixed-modal-close:hover {
                background: #c82333;
                transform: scale(1.1);
            }

            /* Ensure scroll button is above modal */
            #scrollTopBtn {
                z-index: 1000002 !important;
            }

            /* Hidden element for HTML content storage */
            #htmlContentStorage {
                display: none !important;
            }
        `;
        document.head.appendChild(style);

        // 4. FIXED CLICK HANDLER - Separate modal creation function
        function createModal(imageUrl, title) {
            // console.log('Creating modal for:', title);

            // Remove existing modal
            const existingModal = document.querySelector('.fixed-modal');
            if (existingModal) existingModal.remove();

            // Create modal
            const modal = document.createElement('div');
            modal.className = 'fixed-modal';

            modal.innerHTML = `
                <div class="fixed-modal-content">
                    <img src="${imageUrl}" alt="${title}">
                    <div class="fixed-modal-title">${title}</div>
                </div>
                <button class="fixed-modal-close">×</button>
            `;

            // Close handlers
            const closeBtn = modal.querySelector('.fixed-modal-close');
            closeBtn.addEventListener('click', function(e) {
                // console.log('Close button clicked');
                e.stopPropagation();
                modal.remove();
            });

            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    modal.remove();
                }
            });

            // Escape key
            function handleEscape(e) {
                if (e.key === 'Escape') {
                    modal.remove();
                    document.removeEventListener('keydown', handleEscape);
                }
            }
            document.addEventListener('keydown', handleEscape);

            document.body.appendChild(modal);

            // Cleanup escape listener when modal is removed
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.removedNodes) {
                        for (let node of mutation.removedNodes) {
                            if (node === modal) {
                                document.removeEventListener('keydown', handleEscape);
                                observer.disconnect();
                            }
                        }
                    }
                });
            });
            observer.observe(document.body, { childList: true });
        }

        // Function to extract HTML content from the page
        function extractHtmlContent() {
            console.log('🔍 Looking for HTML content in the page...');

            // Method 1: Look for hidden storage element
            const storageElement = document.getElementById('htmlContentStorage');
            if (storageElement && storageElement.innerHTML) {
                console.log('✅ Found HTML content in storage element');
                return storageElement.innerHTML;
            }

            // Method 2: Look for the main content container
            const mainContent = document.querySelector('.output-html, .gr-html, [data-testid="html-output"]');
            if (mainContent) {
                console.log('✅ Found HTML content in main output');
                return mainContent.innerHTML;
            }

            // Method 3: Look for any significant HTML content
            const htmlOutputs = document.querySelectorAll('.prose, .content, .output');
            for (let element of htmlOutputs) {
                if (element.innerHTML && element.innerHTML.length > 1000) {
                    console.log('✅ Found HTML content in generic output');
                    return element.innerHTML;
                }
            }

            console.log('❌ No HTML content found in page');
            return null;
        }

        // 5. SIMPLIFIED CLICK HANDLER - No complex event delegation
        document.addEventListener('click', function(e) {
            const target = e.target;

            // Handle maximize buttons
            if (target.closest('.maximize-button')) {
                e.preventDefault();
                e.stopPropagation();

                const button = target.closest('.maximize-button');
                const imageType = button.getAttribute('data-image-type') || 'Image';
                const imageCard = button.closest('.image-card');

                if (imageCard) {
                    const img = imageCard.querySelector('img');
                    if (img && img.src) {
                        createModal(img.src, imageType + ' Image');
                    }
                }
                return false;
            }

            // Handle save buttons
            if (target.closest('.save-button')) {
                e.preventDefault();
                e.stopPropagation();

                const button = target.closest('.save-button');
                const imageType = button.getAttribute('data-image-type');
                const imageCard = button.closest('.image-card');

                if (imageCard) {
                    const imgElement = imageCard.querySelector('img');
                    if (imgElement && imgElement.src) {
                        const link = document.createElement('a');
                        link.href = imgElement.src;
                        link.download = imageType + '_image.jpg';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        // alert(imageType + ' image saved!');
                    }
                }
                return false;
            }

            // Handle other buttons
            if (target.closest('.close-button')) {
                e.preventDefault();
                // alert('Close functionality');
                const currentPath = window.location.pathname;                
                if (currentPath !== '/' && window.history.length > 1) {
                    window.history.back();
                } else {
                    window.location.href = '/';
                }
                return false;
            }

            if (target.closest('#exportPdf')) {
                e.preventDefault();
                e.stopPropagation();

                console.log('📄 PDF Export button clicked');

                // Extract HTML content from the current page
                const htmlContent = extractHtmlContent();

                if (htmlContent) {
                    console.log('✅ Extracted HTML content, length:', htmlContent.length);

                    // Create a complete HTML document
                    const fullHtml = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Age & Gender Analysis Report</title>
                        <style>
                            body { font-family: system-ui, sans-serif; margin: 20px; }
                            img { max-width: 100%; height: auto; }
                            .image-card { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }
                        </style>
                    </head>
                    <body>
                        <h1>Age & Gender Analysis Report</h1>
                        <p>Generated on: ${new Date().toLocaleString()}</p>
                        <hr>
                        ${htmlContent}
                    </body>
                    </html>
                    `;

                    // Create and download HTML file
                    const blob = new Blob([fullHtml], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = 'age_gender_analysis_' + new Date().getTime() + '.html';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(url);

                    console.log('✅ PDF export completed');
                } else {
                    console.log('❌ No HTML content available for PDF export');
                    alert('No analysis results available. Please run estimation first.');
                }
                return false;
            }
        });

        // 6. Menu functionality
        const menuToggle = document.getElementById('menuToggle');
        if (menuToggle) {
            menuToggle.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                this.classList.toggle('active');
                const mobileNav = document.getElementById('mobileNav');
                if (mobileNav) mobileNav.classList.toggle('active');
                return false;
            };
        }

        // === MOBILE MENU SCROLL CLOSING - ADD THIS EXACT CODE ===
        function closeMobileMenuOnScroll() {
            const menuToggle = document.getElementById('menuToggle');
            const mobileNav = document.getElementById('mobileNav');

            if (menuToggle && mobileNav && mobileNav.classList.contains('active')) {
                console.log('Closing mobile menu on scroll');
                menuToggle.classList.remove('active');
                mobileNav.classList.remove('active');
            }
        }

        // Add scroll event listeners
        window.addEventListener('scroll', closeMobileMenuOnScroll);

        // Also listen to Gradio container scroll
        const gradioContainer = document.querySelector('.gradio-container');
        if (gradioContainer) {
            gradioContainer.addEventListener('scroll', closeMobileMenuOnScroll);
        }
        // === END OF MOBILE MENU SCROLL CLOSING CODE ===

        // 7. TEST: Force scroll button to be clickable
        // console.log('🧪 Testing scroll button functionality...');
        setTimeout(() => {
            const btn = document.getElementById('scrollTopBtn');
            // if (btn) {
            //     console.log('✅ Scroll button exists in DOM');
            //     console.log('📏 Button position:', btn.getBoundingClientRect());
            //     console.log('👆 Button style - pointerEvents:', getComputedStyle(btn).pointerEvents);
            //     console.log('🔝 Button style - zIndex:', getComputedStyle(btn).zIndex);
            // } else {
            //     console.log('❌ Scroll button not found in DOM');
            // }
        }, 1000);

        // Initialize
        function initializeAll() {
            setTimeout(() => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 1000);
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initializeAll);
        } else {
            setTimeout(initializeAll, 100);
        }

        if (window.gradio_app) {
            document.addEventListener('render', function() {
                setTimeout(initializeAll, 500);
            });
        }

        // console.log('✅ Fixed scroll and title positioning setup complete');

        return [];
    }
    """
