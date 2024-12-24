import React, { useState, useEffect } from "react";
import {
  ArrowDown,
  Brain,
  Command,
  Calendar,
  Mail,
  Globe,
  Shield,
  Download,
  Star,
  Cpu,
} from "lucide-react";

const ParticleEffect = () => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none">
    <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-blue-900/20" />
    <div className="particle-container absolute inset-0" />
  </div>
);

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="group relative p-6 rounded-xl bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-lg border border-purple-500/20 transition-all duration-300 hover:scale-105">
    <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity rounded-xl" />
    <Icon className="w-8 h-8 mb-4 text-purple-400" />
    <h3 className="text-xl font-semibold mb-2 text-white">{title}</h3>
    <p className="text-gray-300">{description}</p>
  </div>
);

const TechSpecCard = ({ title, specs }) => (
  <div className="p-6 rounded-xl bg-gradient-to-br from-purple-900/20 to-blue-900/20 backdrop-blur-lg border border-purple-500/20">
    <h3 className="text-xl font-semibold mb-4 text-purple-400">{title}</h3>
    <ul className="space-y-2">
      {Object.entries(specs).map(([key, value]) => (
        <li key={key} className="flex items-center text-gray-300">
          <Cpu className="w-4 h-4 mr-2 text-purple-400" />
          <span className="font-medium">{key}: </span>
          <span className="ml-2">{value}</span>
        </li>
      ))}
    </ul>
  </div>
);

const TestimonialCard = ({ name, role, content, rating }) => (
  <div className="p-6 rounded-xl bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-lg border border-purple-500/20">
    <div className="flex items-center mb-4">
      {[...Array(rating)].map((_, i) => (
        <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
      ))}
    </div>
    <p className="text-gray-300 mb-4">{content}</p>
    <div className="border-t border-purple-500/20 pt-4">
      <p className="font-semibold">{name}</p>
      <p className="text-purple-400">{role}</p>
    </div>
  </div>
);

const InteractiveDemo = ({ activeDemo, setActiveDemo }) => (
  <div className="relative p-6 rounded-xl bg-gradient-to-br from-purple-900/30 to-blue-900/30 backdrop-blur-lg border border-purple-500/20">
    <div className="flex space-x-4 mb-4">
      <button
        onClick={() => setActiveDemo("chat")}
        className={`px-4 py-2 rounded-lg transition-all ${
          activeDemo === "chat"
            ? "bg-purple-500 text-white"
            : "text-gray-400 hover:text-white"
        }`}
      >
        Chat Demo
      </button>
      <button
        onClick={() => setActiveDemo("voice")}
        className={`px-4 py-2 rounded-lg transition-all ${
          activeDemo === "voice"
            ? "bg-purple-500 text-white"
            : "text-gray-400 hover:text-white"
        }`}
      >
        Voice Commands
      </button>
    </div>
    <div className="h-64 p-4 bg-black/50 rounded-lg">
      {activeDemo === "chat" ? (
        <div className="space-y-4">
          <div className="flex items-start space-x-2">
            <div className="bg-purple-500/20 p-2 rounded-lg">
              <p className="text-gray-300">How can you help me with my schedule?</p>
            </div>
          </div>
          <div className="flex items-start space-x-2 justify-end">
            <div className="bg-blue-500/20 p-2 rounded-lg">
              <p className="text-gray-300">
                I can help manage your calendar, set reminders, and coordinate
                meetings with your team. Would you like me to show you how?
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-500/20 animate-pulse" />
            <p className="text-gray-400">Speak now...</p>
          </div>
        </div>
      )}
    </div>
  </div>
);

const ShreeAILanding = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [activeDemo, setActiveDemo] = useState("chat");

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const features = [
    { icon: Brain, title: "Natural Conversation", description: "Engage in fluid, context-aware conversations powered by advanced language models." },
    { icon: Command, title: "Voice Commands", description: "Control your environment with intuitive voice commands and natural responses." },
    { icon: Calendar, title: "Smart Scheduling", description: "Effortlessly manage your calendar with AI-powered scheduling assistance." },
    { icon: Mail, title: "Email Intelligence", description: "Automate email management with smart filtering and response suggestions." },
    { icon: Globe, title: "Multilingual Support", description: "Communicate seamlessly across languages with real-time translation." },
    { icon: Shield, title: "Privacy First", description: "Enterprise-grade security with end-to-end encryption and local processing." },
  ];

  const techSpecs = {
    minimum: {
      os: "Windows 10/macOS 10.15/Ubuntu 20.04",
      processor: "Intel i5/AMD Ryzen 5",
      ram: "8GB RAM",
      storage: "256GB SSD",
      gpu: "Integrated Graphics",
    },
    recommended: {
      os: "Windows 11/macOS 12/Ubuntu 22.04",
      processor: "Intel i7/AMD Ryzen 7",
      ram: "16GB RAM",
      storage: "512GB SSD",
      gpu: "NVIDIA GTX 1660 or better",
    },
  };

  const testimonials = [
    { name: "Sarah Chen", role: "Software Developer", content: "Shree-AI has transformed how I handle my daily tasks. The code assistance is particularly impressive.", rating: 5 },
    { name: "Michael Rodriguez", role: "Product Manager", content: "The calendar management and email features save me hours every week. It's like having a personal assistant.", rating: 5 },
    { name: "Dr. Emily Watson", role: "Research Scientist", content: "The natural language processing capabilities are remarkable. It helps me analyze research papers efficiently.", rating: 4 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-purple-900/20 to-black text-white">
      <nav className={`fixed w-full z-50 transition-all duration-300 ${isScrolled ? "bg-gray-900/95 backdrop-blur-lg" : "bg-transparent"}`}>
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Shree-AI</div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="hover:text-cyan-400">Features</a>
            <a href="#specs" className="hover:text-cyan-400">Specs</a>
            <a href="#demo" className="hover:text-cyan-400">Demo</a>
            <a href="#testimonials" className="hover:text-cyan-400">Testimonials</a>
          </div>
        </div>
      </nav>

      <section className="relative min-h-screen flex items-center justify-center">
        <ParticleEffect />
        <div className="text-center relative z-10">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">The Future of Personal AI</h1>
          <p className="text-xl mt-4">Shree-AI learns, adapts, and grows with you.</p>
        </div>
      </section>

      <section id="features" className="py-16">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>

      <section id="testimonials" className="py-16">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Testimonials</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <TestimonialCard key={index} {...testimonial} />
            ))}
          </div>
        </div>
      </section>

      <section id="specs" className="py-16">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">System Requirements</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <TechSpecCard title="Minimum Requirements" specs={techSpecs.minimum} />
            <TechSpecCard title="Recommended Specs" specs={techSpecs.recommended} />
          </div>
        </div>
      </section>

      <section id="demo" className="py-16">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Interactive Demo</h2>
          <InteractiveDemo activeDemo={activeDemo} setActiveDemo={setActiveDemo} />
        </div>
      </section>

      <footer className="bg-black py-12 text-center">
        <div className="container mx-auto text-gray-400">
          <p>© 2024 Shree-AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default ShreeAILanding;
