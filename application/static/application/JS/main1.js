class MyHeader extends HTMLElement{
    connectedCallback(){
      this.innerHTML = `
        <div class="site-navbar py-2">
          <div class="container">
            <div class="d-flex align-items-center justify-content-between">
              <div class="logo">
                <div class="site-logo">
                  <a href="index.html" class="js-logo-clone">Pharma Friend</a>
                </div>
              </div>
              <div class="main-nav d-none d-lg-block">
                <nav class="site-navigation text-right text-md-center" role="navigation">
                  <ul class="site-menu js-clone-nav d-none d-lg-block">
                    <li class="active"><a href="{% url 'pharmafriend:homepage' %}">Home</a></li>
                    <li><a href="{% url 'pharmafriend:searchpage' %}">Search Medicines</a></li>
                    <li><a href="{% url 'pharmafriend:govmeds' %}">Government Vendors</a></li>
                    <li><a href="{% url 'pharmafriend:pharmacy' %}">Locate Pharmacy</a></li>
                    <li><a href="{% url 'pharmafriend:searchpage' %}">About</a></li>
                    <li><a href="{% url 'pharmafriend:searchpage' %}">Contact</a></li>
                  </ul>
                </nav>
              </div>
              <div class="icons">
              <div class="container">
              <button type="button" class="btn btn-info btn-round" data-toggle="modal" data-target="#loginModal">
                Login
              </button>
                <a href="#" class="site-menu-toggle js-menu-toggle ml-3 d-inline-block d-lg-none"><span
                    class="icon-menu"></span></a>
              </div>
            </div>
          </div>
        </div>
      `
    }
}

customElements.define('my-header',MyHeader)

class MyFooter extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
        <footer class="site-footer">
      <div class="container">
        <div class="row">
          <div class="col-md-6 col-lg-3 mb-4 mb-lg-0">

            <div class="block-7">
              <h3 class="footer-heading mb-4">About Us</h3>
              <p>We are NGO with a mission of providing medicines to the customer at an affordable rate by price comparison and increasing awareness on Medicine prices.</p>
            </div>

          </div>
          <div class="col-lg-3 mx-auto mb-5 mb-lg-0">
            <h3 class="footer-heading mb-4">Quick Links</h3>
            <ul class="list-unstyled">
            <li><a href="{% url 'pharmafriend:homepage' %}">Home</a></li>
            <li><a href="{% url 'pharmafriend:searchpage' %}">Search Medicines</a></li>
            <li><a href="{% url 'pharmafriend:govmeds' %}">Government Vendors</a></li>
            <li><a href="{% url 'pharmafriend:pharmacy' %}">Locate Pharmacy</a></li>
            <li><a href="{% url 'pharmafriend:searchpage' %}">About</a></li>
            <li><a href="{% url 'pharmafriend:searchpage' %}">Contact</a></li>
            </ul>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="block-5 mb-5">
              <h3 class="footer-heading mb-4">Contact Info</h3>
              <ul class="list-unstyled">
                <li class="address">KJSIET Sion, Mumbai, Maharashtra, India</li>
                <li class="phone"><a href="Phone ://+91 77385 74300">+91 77385 74300</a></li>
                <li class="email"><a href="gammabytes.sup@gmail.com">gammabytessup@gmail.com</a></li>
              </ul>
            </div>


          </div>
        </div>
        
      </div>
      <div class="row pt-5 mt-5 text-center">
          <div class="col-md-12">
            <p>
              Copyright &copy;
              <script>document.write(new Date().getFullYear());</script> All rights reserved | Website made by Gammabyte Pvt Ltd.
             
            </p>
          </div>

        </div>
    </footer>`
    }
}

customElements.define('my-footer',MyFooter)