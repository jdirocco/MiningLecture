#!/usr/bin/env python
"""
Quick test script to verify CUDA availability on GPU compute node
Run this with: sbatch just_lunch2.bash test_cuda_on_gpu_node.py
"""
import sys

def main():
    print("="*60)
    print("CUDA AVAILABILITY TEST ON GPU NODE")
    print("="*60)
    
    print('\nPython:', sys.version.split()[0])
    
    try:
        import torch
        print(f'torch: {torch.__version__}')
        print(f'cuda available: {torch.cuda.is_available()}')
        
        if torch.cuda.is_available():
            print(f'cuda device count: {torch.cuda.device_count()}')
            for i in range(torch.cuda.device_count()):
                print(f'  Device {i}: {torch.cuda.get_device_name(i)}')
            print(f'current device: {torch.cuda.current_device()}')
            
            # Test actual CUDA computation
            print('\nTesting CUDA computation...')
            x = torch.randn(1000, 1000).cuda()
            y = torch.randn(1000, 1000).cuda()
            z = torch.matmul(x, y)
            print('✅ CUDA computation successful!')
        else:
            print('❌ CUDA not available on this node!')
            
    except ImportError as e:
        print(f'❌ Could not import torch: {e}')
        sys.exit(1)
    
    try:
        import transformers
        print(f'\ntransformers: {transformers.__version__}')
    except ImportError as e:
        print(f'⚠️  transformers import failed: {e}')
    
    try:
        import bitsandbytes as bnb
        print(f'bitsandbytes: {getattr(bnb, "__version__", "installed")}')
    except ImportError as e:
        print(f'⚠️  bitsandbytes import failed: {e}')
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)

if __name__ == '__main__':
    main()
