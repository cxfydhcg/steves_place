import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Badge } from "../components/ui/badge";

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleOrderOnline = () => {
    navigate("/store");
  };

  const handleCallNow = () => {
    window.open("tel:+1-919-872-2222", "_self");
  };

  const handleAddressClick = () => {
    const address = "6320 Capital Blvd # 119, Raleigh, NC 27616";
    const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;
    window.open(googleMapsUrl, "_blank");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/5 to-secondary/5">
        <div className="container mx-auto px-4 py-8 sm:py-12 lg:py-24">
          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            <div className="space-y-6 lg:space-y-8 text-center lg:text-left">
              <div className="space-y-4">
                <Badge variant="secondary" className="w-fit mx-auto lg:mx-0">
                  🌭 Authentic Flavors Since Day One
                </Badge>
                <h1 className="text-3xl sm:text-4xl lg:text-6xl font-bold tracking-tight leading-tight">
                  Welcome to <span className="text-primary">Steve's Place</span>{" "}
                  🔥
                </h1>
                <p className="text-lg sm:text-xl text-muted-foreground max-w-lg mx-auto lg:mx-0">
                  Home of the finest hotdogs, sandwiches, and comfort food in
                  town. Fresh ingredients, authentic flavors, and a warm
                  atmosphere that feels like home.
                </p>
              </div>

              <div className="flex flex-col gap-3 sm:gap-4 max-w-sm mx-auto lg:max-w-none lg:mx-0 lg:flex-row">
                <Button
                  onClick={handleOrderOnline}
                  size="lg"
                  className="text-base sm:text-lg px-6 py-4 sm:px-8 sm:py-6 w-full sm:w-auto min-h-[48px] touch-manipulation"
                >
                  🛒 Order Online
                </Button>
                <Button
                  onClick={handleCallNow}
                  variant="outline"
                  size="lg"
                  className="text-base sm:text-lg px-6 py-4 sm:px-8 sm:py-6 w-full sm:w-auto min-h-[48px] touch-manipulation"
                >
                  📞 Call Now
                </Button>
              </div>
            </div>

            <div className="relative mt-8 lg:mt-0">
              <div className="aspect-square bg-gradient-to-br from-primary/20 to-secondary/20 rounded-3xl flex items-center justify-center max-w-sm mx-auto lg:max-w-none">
                <div className="text-center">
                  <div className="text-6xl sm:text-8xl lg:text-9xl mb-4 lg:mb-6">
                    🌭
                  </div>
                  <h3 className="text-xl sm:text-2xl font-bold mb-2">
                    Delicious Hotdogs
                  </h3>
                  <p className="text-base sm:text-lg text-muted-foreground">
                    Made Fresh Daily
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 sm:py-16 lg:py-24">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12 sm:mb-16">
            <Badge variant="outline" className="mb-4">
              Why Choose Steve's
            </Badge>
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-4">
              Quality You Can Taste
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground max-w-2xl mx-auto px-4">
              We're committed to serving you the best food with exceptional
              service
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">🥪</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">
                  Fresh Ingredients
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <CardDescription className="text-sm sm:text-base px-2">
                  We use only the freshest, highest-quality ingredients in all
                  our dishes.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">⚡</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">
                  Fast Service
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <CardDescription className="text-sm sm:text-base px-2">
                  Quick preparation without compromising on quality or taste.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0 sm:col-span-2 lg:col-span-1">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">❤️</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">
                  Made with Love
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <CardDescription className="text-sm sm:text-base px-2">
                  Every meal is prepared with care and attention to detail.
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-12 sm:py-16 lg:py-24 bg-muted/50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12 sm:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-4">
              Visit Us Today
            </h2>
            <p className="text-base sm:text-lg text-muted-foreground px-4">
              Come experience the best hotdogs in town
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 max-w-4xl mx-auto">
            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">📍</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">Address</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <button
                  onClick={handleAddressClick}
                  className="text-muted-foreground hover:text-primary transition-colors cursor-pointer underline-offset-4 hover:underline min-h-[44px] px-4 py-2 rounded-md touch-manipulation text-sm sm:text-base"
                >
                  6320 Capital Blvd # 119
                  <br />
                  Raleigh, NC 27616
                </button>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">📞</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">Phone</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <a
                  href="tel:+1-919-872-2222"
                  className="text-muted-foreground hover:text-primary transition-colors underline-offset-4 hover:underline min-h-[44px] px-4 py-2 rounded-md touch-manipulation text-sm sm:text-base inline-block"
                >
                  919-872-2222
                </a>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow p-2 sm:p-0 sm:col-span-2 lg:col-span-1">
              <CardHeader className="pb-4">
                <div className="w-14 h-14 sm:w-16 sm:h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                  <span className="text-2xl sm:text-3xl">🕒</span>
                </div>
                <CardTitle className="text-lg sm:text-xl">Hours</CardTitle>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="text-muted-foreground space-y-1 text-sm sm:text-base px-2">
                  <p>Mon-Sat: 7AM - 6PM</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-background border-t py-8 sm:py-12">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-3 sm:space-y-4">
            <h3 className="text-xl sm:text-2xl font-bold">Steve's Place</h3>
            <p className="text-sm sm:text-base text-muted-foreground px-4">
              Serving delicious food since day one
            </p>
            <div className="pt-3 sm:pt-4 border-t">
              <p className="text-xs sm:text-sm text-muted-foreground">
                Developed by{" "}
                <span className="text-primary font-medium">Xufeng Ce</span>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
