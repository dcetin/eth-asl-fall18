pkg load queueing

function twoMiddlewares(rtt, wtimes, numcli, tmw)
  rtt = rtt ./ 1000.0;
  wtimes = wtimes ./ 1000.0;
  net_thread = 8.5e-6;

  printf("numcli & MW Util & TP & Lat & qlen\n");
  for i = 1:size(wtimes,2)
    numcli(i);
    P = [0 1 0 0; 0 0 0.5 0.5; 1 0 0 0; 1 0 0 0];
    net_delay = rtt(i);
    % net_delay = mean/1000.0;
    S = [net_delay net_thread wtimes(i) wtimes(i)];
    V = qncsvisits(P);
    N = numcli(i);
    m = [0 1 tmw tmw];
    Z = 0;
    [U R Q X] = qncsmva(N,S,V,m,Z);

    mw_util = (U(3) + U(4))/2.0; % utilization
    lat = 1000.0 * (R(1) + R(2) + (R(3) + R(4))/2.0); % response time
    qlen = (Q(3) + Q(4))/2.0; % queue length
    tput = X(3) + X(4); % throughput
    printf("%d & %.3f & %.1f & %.2f & %.2f\n", numcli(i), mw_util, tput, lat, qlen);
    % fprintf('\n')
  end
endfunction

function oneMiddleware(rtt, wtimes, numcli, tmw)
  rtt = rtt ./ 1000.0;
  wtimes = wtimes ./ 1000.0;
  net_thread = 8.5e-6;

  printf("numcli & MW Util & TP & Lat & qlen\n");
  for i = 1:size(wtimes,2)
    numcli(i);
    P = [0 1 0; 0 0 1; 1 0 0];
    net_delay = rtt(i);
    % net_delay = mean/1000.0;
    S = [net_delay net_thread wtimes(i)];
    V = qncsvisits(P);
    N = numcli(i);
    m = [0 1 tmw];
    Z = 0;
    [U R Q X] = qncsmva(N,S,V,m,Z);

    mw_util = U(3); % utilization
    lat = 1000.0 * (R(1) + R(2) + R(3)); % response time
    qlen = Q(3); % queue length
    tput = X(3) ; % throughput
    printf("%d & %.3f & %.1f & %.2f & %.2f\n", numcli(i), mw_util, tput, lat, qlen);
    % fprintf('\n')
  end
endfunction

% % mwb2-wo-64
% rtt = [3.048 3.525 3.655 2.808 2.133 2.085 2.097];
% wtimes = [3.4 3.2 4.0 5.5 7.9 11.6 12.0];
% numcli = [6 24 48 72 96 192 288];
% tmw = 64;
% twoMiddlewares(rtt, wtimes, numcli, tmw)

% % mwb2-ro-8
% rtt = [4.149 3.885 3.806 3.525 3.488 3.372];
% wtimes = [1.7 1.7 2.0 3.5 5.0 5.4];
% numcli = [6 12 18 24 48 192];
% tmw = 8;
% twoMiddlewares(rtt, wtimes, numcli, tmw)

% % mwb1-wo-64
% rtt = [2.304 2.501 3.151 2.719 2.503 2.565];
% wtimes = [2.9 2.7 3.3 5.1 6.4 7.4];
% numcli = [6 24 48 72 96 192];
% tmw = 64;
% oneMiddleware(rtt, wtimes, numcli, tmw)

% % mwb1-ro-64 
% rtt = [3.737 3.602 2.67  2.536 2.72  2.64 ];
% wtimes = [1.3 1.2 5.0 12.7 21.1 21.6];
% numcli = [6 12 24 48 96 192];
% tmw = 64;
% oneMiddleware(rtt, wtimes, numcli, tmw)