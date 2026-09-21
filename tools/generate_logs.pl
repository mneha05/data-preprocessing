#!/usr/bin/env perl
use strict;
use warnings;
use JSON::PP;
use Time::HiRes qw(time);

my $count = shift // 1000;
my @services = qw(inference preprocessor scheduler gateway);
my $json = JSON::PP->new->canonical;

srand(7);
for (my $i = 0; $i < $count; $i++) {
    my $service = $services[int(rand(@services))];
    my $gpu_id = int(rand(4));
    my $latency = 2 + rand(35);
    my $requests = 50 + int(rand(500));
    my $errors = rand() < 0.04 ? 1 + int(rand(3)) : 0;

    print $json->encode({
        ts => time(),
        service => $service,
        gpu_id => $gpu_id,
        latency_ms => 0 + sprintf("%.3f", $latency),
        requests => $requests,
        errors => $errors,
        gpu_util_pct => int(30 + rand(70)),
        memory_mb => int(1000 + rand(12000))
    }), "\n";
}
